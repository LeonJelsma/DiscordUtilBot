<h1> Utility bot for Discord </h1>

A Discord bot used for various generic functions. This was intended for private use, but I decided to make this repo open-source so anyone could use it and see how the bot works internally. The bot was made using Python 3.7.0. It utilizes a local SQLite database for storing an index to the .wav files added to the bot. This database is also used to store keywords, responses and admins. Two external API's are used to supply the bot with random cat facts and weather information. The weather API requires an API key to be used.

<ul>
  <li>Playing .wav files</li>
  <li>Reading text from images</li>
  <li>Admin system</li>
  <li>Pick playing cards</li>
  <li>Generate weather reports</li>
  <li>Respond keywords</li>
  <li>More!</li>
 </ul>


<h2> Usage </h2>

<ol>
  <li>Run start.bat to generate an empty config.json (Located at [BOT_DIR]/resources/config/json.config)</li>
  <li>Open json.config</li>
  <li>Token: This is where you place your Discord Oauth2 token<lo/>
  <li>Weather_key: To use the "!weather" function this field needs to be supplied with an API key from <a href=https://openweathermap.org/api>OpenWeatherMap</a></li>
  <li>Tesseract_Location: To use the "!read" function on an image this field needs to be supplied with a path to "tesseract.exe" download tesseract-ocr from <a href=https://tesseract-ocr.github.io/tessdoc/Home.html>their website</a></li>
  <li>Owner_id: Place your unique Discord user ID here</li>
</ol>
