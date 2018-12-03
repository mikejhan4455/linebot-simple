# LineBot simple deployment

- usage

  1. download sources

  ```bash
  git clone https://github.com/mikejhan4455/linebot-simple.git
  ```

  2. configure

      - /env-file/linebot.env

        paste the channel **access token & channel serect** of  your lineBOT

        find it @  [line develop console](https://developers.line.biz/console/)

        ```shell
        CHANNEL_ACCESS_TOKEN=<YOUR_LINEDEV_CHANNEL_ACCESS_TOKEN>
        CHANNEL_SERECT=<YOUR_LINEDEV_CHANNEL_SERECT>
        ```

     - /env-file/ngrok.env
       paste the **Channel access token** of your Ngrok account 

       find it @ [ngrok auth](https://dashboard.ngrok.com/auth)

       ```shell
       NGROK_PORT=3001
       NGROK_AUTH=<YOUR_NGROK_TUNNEL_AUTHTOKEN>
       NGROK_REGION=ap
       ```

  3. run the server

     ```bash
     docker-compose up
     ```


