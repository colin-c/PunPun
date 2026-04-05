# PunPun

A Discord bot with a simple `!pp` command prefix.

## Features
#### Hello
!pp hello *(returns `hi @user` inside a code block box)*

#### Choose
!pp riot *(chooses between League or Valorant)*

#### Coin
!pp coin *(flips a coin and returns Heads or Tails)*

#### Slur Tracker
!pp @user slur *(increments that user's count by 1 and shows the total)*
!pp @user slur count *(shows the current total without incrementing)*
!pp @user slur reset *(sets the total to 0)*
!pp @user slur minus {value} *(subtracts a value, default 1, never below 0)*

#### Stock
!pp stock {ticker} *(returns the live ticker, company name, exchange, current price, today high, and today low)*

#### Music
!pp play {youtube link} *(joins your voice channel and plays the link)*
!pp play {spotify link} *(uses the Spotify track title to find the closest playable match)*
!pp play {title} *(searches YouTube for the closest match and plays it)*
!pp continue *(resumes paused audio)*
!pp queue *(shows the current track and the next few tracks waiting)*
!pp pause *(pauses the current track)*
!pp skip *(skips the current track and starts the next one)*
!pp disconnect *(disconnects the bot from voice)*

## Setup
Install dependencies with `python -m pip install -r requirements.txt`.
You also need `ffmpeg` installed and available on your `PATH` for voice playback.
