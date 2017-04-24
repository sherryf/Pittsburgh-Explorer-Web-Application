var twilio = require('twilio');

// Find your account sid and auth token in your Twilio account Console.
var client = twilio('AC1d38e85ac70edb619594a06caec1ff00', '6f96fdcd9b11ffa5882be82a0dda5769');

// Send the text message.
client.sendMessage({
  to: '+16502502374',
  from: '+12053040467',
  body: 'can we do this!'
});
