AI-House

AI-House is a "game" made in Unity wherein AI chatbots trained with DialoGPT can interact with each other. The bots are fine-tuned with training data from Kaggle TV script datasets, so they talk like popular TV characters. In the simulation, they will interact and form relationships with each other based on the sentiment of what they say to each other, as well as interact with their environment and make art with CLIP.

To start out, these actions will be performed by parsing a response from asking the bot questions about what it wants to do and what kind of decisions it wants to make.

Eventually, once I learn a bit more about Pytorch, a better model will be developed to handle these specific scenarios for this game in particular, and I'll just be able to query the model to have it decide what to do.

For now, here is a high-level roadmap of the game design:

-populated with 6 AI characters
	-characters are created from either chat or tv show/movie transcripts
	-personality is determined from this too
		-attributes TBD
			-some are unchangable, some can change
		-have a couple of "top favorite things"
-character interactions are narrated in the game log
	-character actions are narrated in their character log
-characters talk to each other and form frienships based on sentiment of conversation and personality
	-if characters are good enough friends they can do activities together
	-characters talk to each other about their creations
	-character chat logs can be viewed
	-user can also click on a character to chat with them and ask them about the house/other characters or whatever else
-characters do various activities in the house
	-make art
	-write stories
	-cook
	-watch TV/movies
	-listen to music
	-play video games
	-can click on character to see what movie/show/music/game they are doing
-characters decorate their room and the living space how they want
	-characters vote on common living space decorations/look
		-they can vote to have other characters' art displayed on the wall
	-changes over time depending on characters' actions/personality changes
-random events happen that the characters respond to
	-random visitors/solititors to the house
-simulation lasts for a certain amount of time, and at the end statistics are listed for
	-most liked character
	-characters' accomplishments/creations
	-final image of house is also displayed
	
-model
	-personality, action and sentiment changes based on interactions with other characters
