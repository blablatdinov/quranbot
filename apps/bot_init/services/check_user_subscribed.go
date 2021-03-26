package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/zenthangplus/goccm"
)

type Subscriber struct {
	ChatId       int64 `db:"tg_chat_id"`
	IsSubscribed bool  `db:"is_active"`
}

type TelegramAnswer struct {
	ok bool `json:"ok"`
}

func GetSubscribersList() []Subscriber {
	db, err := sqlx.Open("postgres", "user=qbot password=qbot host=localhost port=5123 dbname=postgres sslmode=disable")
	if err != nil {
		fmt.Print("oops")
	}
	var subscribers []Subscriber

	query := "SELECT s.tg_chat_id, s.is_active FROM bot_init_subscriber as s"
	err = db.Select(&subscribers, query)
	if err != nil {
		fmt.Print(err.Error())
	}
	return subscribers
}

func CheckIsSubscriber(chatId int64) (bool, error) {
	url := fmt.Sprintf("https://api.telegram.org/bot452230948:AAF4k2UPJ9yiG_E8Nhx3ovWyVQVy4F4J6SM/sendChatAction?chat_id=%d&action=typing", chatId)
	response, err := http.Get(url)
	if err != nil {
		fmt.Println(err.Error())
		return false, err
	}
	var ans TelegramAnswer
	responseBody, _ := ioutil.ReadAll(response.Body)
	json.Unmarshal(responseBody, &ans)
	return ans.ok, nil
}

func main() {
	subscribers := GetSubscribersList()

	c := goccm.New(3)

	for _, subscriber := range subscribers {
		c.Wait()
		go func(subscriber Subscriber) {
			is_active, _ = CheckIsSubscriber(subscriber.ChatId)
			c.Done()
		}(subscriber)
	}
	c.WaitAllDone()
}
