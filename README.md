# chatNLPapi

This is the story of a failure...

I created an API that used a pre-built NLP model from Flair library to process messages from a MongoDB Atlas database, filled with fake chats. I really enjoyed comparing pre-built NLP models from different libraries, as my goal is to produce my own models as soon as I take my first bites of the ML pizza (happily, it is gonna happen 12 hours after I finish writing this file). Yeah, my API was cool, this was quite a cool project... But then the nightmare began.

I could create a Docker image of my API and have it serving from local. I even deployed it in Heroku and everything looked fine. However, dark mysteries were awaiting.

This is the message that has chased me eversince: /bin/sh: 1: rails: not found. The API was not working properly, and only this command could at least show why: heroku run rails console. I could count on the workforce of more than 200 developers on Stack Overflow and GitHub forums, but no one could help me. Rails in the bin folder were missing, and no rails commands were apparently available for me. Heroku DevCenter suggested that maybe this potion could bring me back to life: bundle exec rake rails:update:bin. However, a kafkian version of Apple blocked my way. "You don't have write permissions for the /Library/Ruby/Gems/2.6.0 directory", they said, and the Stack Overflow community, just as people from the village that lies under the castle that Kafka dreamt of, repeated the words of their masters: "While it's OK to make minor modifications to that if you know what you're doing, because you are not sure about the permissions problem, I'd say it's not a good idea to continue along that track." Oh, Ruby, gift of the gods, why are you hiding from me? When will I be able to perform your magic and create that miserable bin folder that denies my glory?

We will see each other soon...