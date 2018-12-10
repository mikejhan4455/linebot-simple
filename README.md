# [LineBot simple deployment](https://github.com/mikejhan4455/linebot-simple)

## Features

- Simplify the deployment to a Line Bot service
- Building a Line Bot without writing codes
- Config the reaction with query in Key - Value mapping

The application is tested under docker image [ubuntu:18.04](https://hub.docker.com/_/ubuntu/)
Might be able to run under other operating systems with docker

## Usage

Create a application of Line Bot and a webhook server to handle the line message webhook event. Combine these as a line bot service.

- container `handler` : The packed linebot handeler server
- container `ngrok-server` : Webhook server with SSL using [Ngrok](https://ngrok.com/)

## Build

###Requirement:

- Docker

  - MacOS

    ```powershell
    brew install Docker
    ```

  - Ubuntu

    ```
    apt-get install Docker
    ```

- Docker-composer

  See [Install composer](https://docs.docker.com/compose/install/#install-compose).

### How to:

1. Clone this repository:

   ```git clone https://github.com/mikejhan4455/linebot-simple```
2. Go inside the folder
   ```cd/dir linebot-simple```

3. Config

   - ```/env-file/linebot.env```

     Paste the **Channel access token & Channel serect** of  your line channel.

     You can find it at  [line develop console](https://developers.line.biz/console/)

     ```shell
     CHANNEL_ACCESS_TOKEN=<YOUR_LINEDEV_CHANNEL_ACCESS_TOKEN>
     CHANNEL_SERECT=<YOUR_LINEDEV_CHANNEL_SERECT>
     ```

   - ```/env-file/ngrok.env```

     Paste the **Channel access token** of your Ngrok account.

     Your can find it at [Ngrok auth](https://dashboard.ngrok.com/auth)

     ```shell
     NGROK_PORT=3001
     NGROK_AUTH=<YOUR_NGROK_TUNNEL_AUTHTOKEN>
     NGROK_REGION=ap
     ```

4. Run the server with docker-compose

```docker-compose up```