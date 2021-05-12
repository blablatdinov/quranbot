// GOOS=linux GOARCH=amd64 go build -o check_users main.go

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/jmoiron/sqlx"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

type Subscriber struct {
	Id       int  `db:"id"`
	ChatId   int  `db:"tg_chat_id"`
	IsActive bool `db:"is_active"`
}

type TelegramActionResponse struct {
	Ok           bool   `json:"ok"`
	ErrorCode    int    `json:"error_code"`
	Description  string `json:"description"`
	ChatId       int
	SubscriberId int
	WasActive    bool
}

func getSubscribers(dbPath string) []Subscriber {
	var subscribers []Subscriber
	db, err := sqlx.Connect("postgres", dbPath)
	if err != nil {
		log.Fatal(err.Error())
	}
	query := "select id, tg_chat_id, is_active from bot_init_subscriber"
	err = db.Select(&subscribers, query)
	if err != nil {
		log.Fatal(err.Error())
	}
	return subscribers
}

func checkSubscriberStatus(subscribers []Subscriber) []TelegramActionResponse {
	telegramBotToken := os.Getenv("BOT_TOKEN")
	checkThreadsCount, err := strconv.Atoi(os.Getenv("CHECK_SUBSCRIBERS_STATUS_THREADS_COUNT"))
	if err != nil {
		log.Fatal(err.Error())
	}
	ch := make(chan TelegramActionResponse, len(subscribers)) // buffered
	limit := make(chan struct{}, checkThreadsCount)
	var responses []TelegramActionResponse
	for _, subscriber := range subscribers {
		go func(subscriber Subscriber) {
			var responseBody TelegramActionResponse
			limit <- struct{}{}
			url := fmt.Sprintf("https://api.telegram.org/bot%s/sendChatAction?chat_id=%d&action=typing", telegramBotToken, subscriber.ChatId)
			resp, err := http.Get(url)
			defer resp.Body.Close()
			json.NewDecoder(resp.Body).Decode(&responseBody)
			responseBody.ChatId = subscriber.ChatId
			responseBody.SubscriberId = subscriber.Id
			responseBody.WasActive = subscriber.IsActive
			if err == nil {
				resp.Body.Close()
			}
			ch <- responseBody
			<-limit
		}(subscriber)
	}

	for {
		r := <-ch
		responses = append(responses, r)
		if len(responses) == len(subscribers) {
			return responses
		}
	}
	return responses
}

func serviceResponses(responses []TelegramActionResponse, dbPath string) {
	db, err := sqlx.Connect("postgres", dbPath)
	if err != nil {
		log.Fatal(err.Error())
	}
	nowDateTime := time.Now().Format("2006-01-02 15:04:05-07")
	query := "update bot_init_subscriber set is_active='f' where "
	query2 := "insert into bot_init_subscriberaction (subscriber_id, action, date_time) values "
	insertparams := []interface{}{}
	updateparams := []interface{}{}
	for _, response := range responses {
		if !response.Ok && response.WasActive {
			fmt.Printf("Subscriber: %d unsubscribed\n", response.ChatId)
			query = query + fmt.Sprintf("tg_chat_id=%d or ", response.ChatId)
			query2 = query2 + fmt.Sprintf("(%d, 'unsubscribed', '%v'),", response.SubscriberId, nowDateTime)
		}
	}
	if len(query) >= 52 && len(query2) >= 81 {
		queryUpdate := query[:len(query)-4]
		fmt.Println(queryUpdate)
		res := db.MustExec(queryUpdate, updateparams...)
		fmt.Println(res)
		queryInsert := query2[:len(query2)-1]
		fmt.Println(queryInsert)
		res = db.MustExec(queryInsert, insertparams...)
		fmt.Println(res)
	}
}

func activeUsers(dbPath string) {
	db, err := sqlx.Connect("postgres", dbPath)
	if err != nil {
		log.Fatal(err.Error())
	}
	row := db.QueryRow("select count(*) from bot_init_subscriber where is_active='t'")
	var activeSubscribersCount int
	err = row.Scan(&activeSubscribersCount)
	if err != nil {
		log.Fatal(err.Error())
	}
	row = db.QueryRow("select count(*) from bot_init_subscriber")
	var totalSubscribersCount int
	err = row.Scan(&totalSubscribersCount)
	if err != nil {
		log.Fatal(err.Error())
	}
	fmt.Printf("Total subscribers count: %d\nActive subscribers count: %d\n", totalSubscribersCount, activeSubscribersCount)
}

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	dbPath := os.Getenv("DATABASE_URL")
	subscribers := getSubscribers(dbPath)
	responses := checkSubscriberStatus(subscribers)
	serviceResponses(responses, dbPath)
	activeUsers(dbPath)
}
