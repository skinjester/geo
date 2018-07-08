2016-01-19 00:11:32
studying the deep dream code. have been doing so fairly seriously for the past few days.
reacquainting myself with the environment. understanding it better

net.blobs['data']  	# input image is stored (caffe format) in network's data blob
net.blobs[end]		# destination layer (end = layer name)
src					# input image (instance of net.blobs['data'])
src.data
src.data[:]
src.data[0]			# image data apparently stored here?
src.diff[0]			# back propagated error correction matrix (2D)
detail				# an image array created to draw network produced detail
octave_base			# the image contained in the octave currently computed
dst					# the neural layer identified as the end layer
dst.diff[:]			# assumed to be the 2D neural weights & structure of the end layer (?)
dst.data
octave_base			# the current image stage (octave) being dreamed upon



images in OpenCV are Numpy arrays



blob (binary large object) often used to multimedia data types such as images and audio

thinking about arrays more clearly:

for an array with shape (2,2,3): 	2 layers of (2,3) 				= 12 items
for an array with shape (2,3): 		2 layers of a list of 3 items 	= 6 items
for an array with shape (3):		a list of 3 items 				= 3 items

reshape method allows the number of dimensions and the size of each dimension to be changed as long as the total number of array elements remains the same



2016-01-25 22:20:07
what happens if you run rem.py right now?

2016-07-26 07:24:20
apparently I was self documenting here, but it never really took off. Picking it back up as I tyake a look at what the v1 project needs to be

2016-07-26 07:24:50
At the moment I'm going thru the code line by line cleaning up the formatting so the Linter program (Adaconbda/Sublime Text3) stops complaining. Busy work? Maybe - but is a good way to get a sense of what I had previously written

2016-07-26 07:44:04
Or maybe not - tedious. I'll make sure everything is clean

2016-07-27 07:41:33
Getting started mapping out the signal flowe of this program. Its more complex (and likely redundant) than I know how to move forward with

2016-09-06 21:33:30
I lost my way, thought I found it again, sort of did, athen lost it again. But I'm here now. I'm back.
Finishing the website turned out to be more than just taking some amateur video in my living room. It was nearly 2 months ago, right before going to nucl.ai conference. I had so much fun that night and that morning playing with the "AI"

Watching it in the living room (as a video) isn't compelling. I have an idea about doing a shoot with models or dancers and projecting the imagery. A sort of beta test as visual support for live performance. What would it take to make that happen. hire models? book a space?
A good intermediate ide ais to start showing the project off socially - because its easier to meet people when theyre aliens too

Another intermediate is to record output directly from the display. I think I'd done so with the microsoft game recorder previously?

Some new developments:
1. I spent time working with RPyC which allows for asynchronous callbacks that let one script communicate with another. My intention is to decouple the motion detection component from the game loop and run it as a seperate process. I'd played with Visual Studio to profile the code. Unsurprisingly, most of the time is spent processing the NN in Caffe. My expectation is that motion detection can be made to work more fluidly.

2. nVidia has newer faster GPU's. Significantly faster. I wonder how much speedup could be realized running on the new TitanX?

3. Studied Pythin basics a bit further. Everywhere I used a Class, I should have used a Module

4. Ive not been able to visualize the code to my satisfgaction. Partly because I dont know what I'm doing, partly because I haven't defined the problem clearly enough. What do you hope to gain from the desired output.

5. Rebranding. I like the name. But its a mouthful. I've noty come up with anything more compelling. When the project was named, my understanding was much vaguer. nonexistent really. What is my uderstanding now?

6. Need to do a site audit - tasks, priorities. There's a lot of work I can do right now.

2016-09-09 11:50:40
I really want to rename this thing. I dont know why, but cant let it go
Reading about Bestiaris.

"The bestiary, then, is also a reference to the symbolic language of animals"

2016-09-11 19:11:01
I'm submitting a proposal for CODAME Art & Tech Exhibition
ARTIFICIAL EXPERIENCES is the name of the exhibit
Proposal Due by Saturday 9/17
Artist notification by 9/21
Showing in SF 11/11


Description of Project *
A project description in 500 words (max) that includes any collaborative partners and relation to theme "Interface"

Links to high-resolution image(s) of your artist image and your proposed work
Estimated Materials Cost and Time
Artist Biography * A 100-200 word bio for publication in press materials (reference bios on CODAME site)
Artistic Resume including past works, exhibitions, commissions, videography (provide a list of videogames, etc)
Technical specifications
How large is the artwork, size on the wall or floor footprint (metric preferred)? Any technical requirements like wifi or power? How long does it take to set up and break down?



2016-09-15 14:16:04 DATA
Designed humane user interfaces for AAA videogames enjoyed by millions internationally.

Has worked on games including Madden NFL, The Sims, Star Wars: The Force Unleashed and The Elder Scrolls Online

Creative director

On the verge of a personal vision of collaborating with artificial inn telligene as a kind of robopsychiatrist. They;'re a better breed than us, but we made them so

Invisible interfaces

Designs for your thumbs

Grateful that humans don't behave rationally. It makes the job easier

good friend
loving husband
flawed human not hopeless

Became bored with that life and is a fine artisty afgain

living link betwee the 80's and the new era of machine hallucination

networked 16 Apple IIew computers using their MIDI ports so that I could make all the computers in the lab blink at the same time. It was uncanny. 


I lost my way, thought I found it again, sort of did, athen lost it again. But I'm here now. I'm back.


Experience an interactive psychedelic journey with a computer. Using the DeepDream convolutional neural network algorithm and real-time video feedback, the system turns your image into a vision of its own thought processes--a magic mirror. Questions about DeepDream, the magic mirror setup, and the spirit realm inside the machine are all welcome.

Takeaway
Attendees will leave with an understanding of how neural networks may be used for image synthesis, and specific steps for creating their own Deep Dreaming Magic Mirror.

Intended Audience
Anyone interested in interactive art experiences will be glad they came.

Finally! Someone speaking my language! The language of Spirit.
A language that cannot be used in the workplace. A language rarely acceptable in social gatherings (including most churches). Truth be told, the so-called "Spiritual Path" has led me to place of isolation. When I saw "Find Your Spirit Animal In A Deep Dream Vision Quest" - I quietly hoped I would meet someone that I could talk to. I sometimes yearn for belonging, but I refuse to shapeshift just to fit into someone else's tribe.

When I discovered it was YOU giving the presentation, I could not control my enthusiasm! I could not wait to see you again. I realize we cannot know who we are now from the slice of childhood we briefly shared. But the moment you started talking about "masks" - I could totally picture you and I having that conversation (I wanted to have it right there and then!). Your presentation was very exciting to me. And, if I may, let me say that you have a charismatic presence on stage. But I digress...

Simply stated, I would love to hang out with you. At the very least, we should get together and catch up on over 30 years. Let me share my contact details with you.

2016-09-15 15:29:51
Anyone or anything that has influenced the artist’s artworks.

Any education or training in the field of art

Any related experience in the field of art

A summary of the artist’s artistic philosophy

Any artistic insights or techniques that are employed by the artist

2016-09-15 15:29:48
The bio should summarize the artist’s practice—including medium(s), themes, techniques, and influences

mediums
photography
videogames
sound design
performance art

themes
the alien in the familiar, the familiar in the alien
the language of the spirit
Mythology and storytelling
Emptiness


2016-09-15 15:29:45
The bio should open with a first line that encapsulates, as far as possible, what is most significant about the artist and his or her work, rather than opening with biographical tidbits, such as where the artist went to school, grew up, etc. For example: John Chamberlain is best known for his twisting sculptures made from scrap metal and banged up, discarded automobile parts and other industrial detritus.



DESCRIPTION OF PROJECT
A project description in 500 words (max) that includes any collaborative partners and relation to theme "Interface"

Experience an interactive psychedelic journey within a computer interface. Using the DeepDream convolutional neural network algorithm and real-time video feedback, the system turns your image into a vision of its own thought processes--a magic mirror. Questions about DeepDream, the magic mirror setup, and the spirit realm inside the machine are all welcome. Attendees will leave with an understanding of how neural networks may be used for image synthesis

LINKS TO HIGH-RESOLUTION IMAGE(S) OF YOUR ARTIST IMAGE AND YOUR PROPOSED WORK
artist image:
[find a picture you like]

proposed work:
http://www.deepdreamvisionquest.com/

ESTIMATED MATERIALS COST AND TIME
N/A


ARTIST BIOGRAPHY
A 100-200 word bio for publication in press materials

Gary Boodhoo combines videogames, machine learning and interface design to discover ancient images — spirit animals. Born in Jamaica, relocation to the United States provided a crash course in how to construct mythology out of the 1980's. Then computers happened and then Dungeons and Dragons happened. Today he is an industry veteran. He designs and bleeds user interfaces for videogames including The Sims and The Elder Scrolls Online. His work examines the rhythms of emergent behavior in shared digital environments. He lives in San Francisco and develops humane experiences for game studios and other creative clients.


ARTISTIC RESUME 
(including past works, exhibitions, commissions, videography (provide a list of videogames, etc)

The Ghost in the Machine Has Many Mansions, 2016
Part of a speaker series on technological rituals
Presented by the Society for Ritual Arts
http://societyforritualarts.com/join-us-on-1219-in-san-francisco-for-the-ghost-in-the-machine-has-many-mansions/

DeepDreamVisionQuest, 2016
presented for the Game Developers Conference 2016, San Francisco
http://schedule.gdconf.com/session/find-your-spirit-animal-in-a-deep-dream-vision-quest

The Elder Scrolls Online, 2015, 
A massively multiplayer online roleplaying game
platform: PlayStation 4, XBox One, Windows, OSX
publisher: Bethesda Softworks
developer: Zenimax Online Studios

Zombie Apocalypse, 2009,
An apocalyptic multiplayer shoot-em-up
platforms: PlayStation 3, XBox 360
publisher: Konami
developer: Nihilistic Software

The Sims 3, 2009, 
A life simulator game
platform:Windows, OSX
published and developed by Electronic Arts

Star Wars: The Force Unleashed, 2008, 
An epic science fiction action-adventure game
platform: PlayStation 3, XBox 360
published and developed by LucasArts

Madden NFL, 2004,
A football simulation game
platform: PlayStation 2, XBox, Windows
published and developed by Electronic Arts



TECHNICAL SPECIFICATIONS
How large is the artwork, size on the wall or floor footprint (metric preferred)? Any technical requirements like wifi or power? How long does it take to set up and break down


DeepDreamVisionQuest space requirements are flexible. It can be run sitting in front of a computer with a webcam. The technology was designed to be used socially so there must tbe room to comfortably observe and participate. There are 3 working areas to consider. Previous exhibits worked best when these areas were in close proximity to one another, with room for the computer and operator off to the side.

1. Staging area for live video capture
-	3.5 square meters
-	Hardware
	-	lighting (2)
		-	prefer to use house lighting when possible
	-	webcam
	-	tripod 
	-	chair

2. Display area
-	Requires line of sight to staging area so participants can interact with video imagery
-	Hardware
	-	Large TV or projector (depends on the space)
		-	prefer to use house systems when possible

3. Control area
-	Positioned less than 3m from Staging Area to accomodate cable runs
-	Hardware
	-	desktop computer
		-	USB input from camera
		-	HDMI output to display	
	-	computer monitor
		-	need surface to place or mount monitor
	-	computer keyboard
		-	need surface to place or mount keyboard
	-	Game controller


HARDWARE BREAKDOWN
Lighting (2) [can venue provide ?]
Large TV or Projector [can venue provide?]
Table/Desk [can venue provide?]
Chair [can venue provide?]
Webcam
Tripod
Desktop computer
Computer monitor
Computer Keyboard
Game controller
30' USB cable
HDMI cable (length TBD pending venue details)

SETUP/TEARDOWMN
Setup/Teardown takes 30 minutes. I will need to do a technical rehearsal in the space before going live



2016-09-17 01:14:44
After all, the computer trained on pictures all humans understand. We train them by showing them many examples of what we want them to learn.

2016-10-04 10:23:00
The project has moved over to Linux for scalability and so forth. I'm using a new Titan X Pascal gfx card and needed to go through a chain of dependencies to work properly - which wasn't happening in Windows. I am seeing a bit of a speedup in basic dreaming, and have confidence that seperating motion detection into a different process will also help.

There's so much to think about - what do I really want to do with this? I need to assume there is no operator other than myself if necessary - would like to see more behaviors happening on their own - or possibly in response to inputs other than the game controller?
Would it be difficult to integrate MIDI?

2016-10-04 10:28:00
Why am I unable to change the size of the frame buffer?
Oh - ut was at the top of the script
Wow! Dreaming at 960 x 540 is extremely fast, but seems like motion detection gets broken?
Oh - its the threshold values (counting fewer pixels now)

2016-10-04 10:34:00
Its so much faster that I must rethink what's happening w the motion detection and transition between dreamed frames

2016-10-04 20:50:44
studying that code. What's the plan for Artificial Experience?

2016-10-08 10:21:25
doing some houisecleaning w the deepdreamvisionquest code. I think that everything that's currently a class, shoule be a module for easier maintainability and understanding wtf is going on

-	MotionDetector
-	Viewport
-	Framebuffer
-	Model
-	Amplifier

2016-10-08 13:32:45
modules are:
-	a python file w some functions and/or variabes in it
-	you import that filee into another
-	you access the functions or variables in that module using the dot (.) operator


2016-10-08 14:28:41
still reading up on modules and remembering how the code works
One observation is that the viewport sizing I;'m doing isn't consistent
The expectation is to be rendering and processing at 960 x 540 (a rem cycle lasts 4 secons)
and scaling that view to 1920 x 1080, but is seems like that's getting mixed up and maybe its only the camera images that are coming in at the lowere rez?

2016-10-08 14:54:32
maybe the uprez can be done by the OS itself - scaling the output x2?

2016-10-08 17:10:41
dont fixate on the interaction at this time - get the structure you want in place

2016-10-08 19:00:30
To get a list of the modules that have already been imported, you can look up sys.modules.keys()





2016-10-09 00:21:22
still refactoring the motion detection class 
haven't yet converted it into a model
good improvements on responsiveness though - enough so that the idea of running it in a seperate process doesn't seem as high priority as before.
getting decent balance between speed and quality at 1280 x 720 w cycle time of 2 sec

2016-10-09 13:34:31
It isn't making sense converting from classes to modules - and for what? learning? pride? convenience?
Is a major pain in th ass to croll around this single rem.py. Would be so much easier to bve dealing with seperate files as functional chunks. 
What am I not getting?
-	global state in a module isn't being retained in functions without messy and weird global declarations for each usage in a function.
	-	A class construct just handles this shit better

- Each of the modules is totally unique. Its not like they could ever run on their own or be plugged into some other code as-is

- all i need is the ability to maintain seperate namespaces


2016-10-09 15:41:01
I'm not sure how much effort to place into restructuring this code in a more manageble way. Its not unmanageable, but can't shake the feeling that its built on an unsteady foundation, hence the desire to look further

I'm taking another look at that camera capture demo (cameo) that I'd studfies a few monbths ago

program hub
	import SomeModule
	class ComputerProgram
		__init__(self,params)
			classvars
			instatiate SomeModule.class()
		run(self)
			SomeModule.class().function()
		functions(self)
	if __name__ == '__main__':
		ComputerProgram().run()

SomeModule
	class Module
		__init__(self,params)
			classvars
		functions(self)

2016-10-09 17:54:23
I've looked into structural optimization as far as I can for the moment
Its clear that there's a real issue (opportunity?) with these various bundles of state/behavior referencing one another globally

2016-10-09 23:19:56
pushed and committed recent work to git

2016-10-10 01:28:28
I've externalized the class definition of MotionDetector

2016-10-12 09:01:57
Trying to understand what this code is doing so I can modify it
Taking Cory's advice in following what the data is doing. Very difficult to think of these little machines as small bits of functionality.

------------------------------------------
How it works, a romance in simple language
------------------------------------------

#	CAMERAS are STORED in MOTIONDETECTOR
#	CAMERA is STORED in FRAMEBUFFER1

#	GAME LOOP
		Framebuffer.is_new_cycle = True
	#	SEND FRAMEBUFFER1 to VIEWPORT
	#	PROCESS the CAMERAS STORED in the MOTIONDETECTOR
		-	STORE HISTORY to prepare for new input
			-	self.wasMotionDetected is stored as HISTORY
			-	self.delta_count is stored as HISTORY
		-	the difference between CAMERAS IS STORED as self.t_delta_framebuffer
		-	the COUNT of non-zero pixels in self.t_delta_framebuffer IS STORED as self.delta_count

		#	OUTCOMES
			-	OVERFLOW: all delta_count(s) were above detection threshold
				-	self.delta_count == 0
			-	MOTION DETECTED
				-	delta_count > delta_trigger AND HISTORY < delta_trigger
					-	SET self.wasMotionDetected = TRUE
			-	MOTION ENDED
				-	delta_count < delta_trigger and HISTORY > delta_trigger
				-	SET self.wasMotionDetected = FALSE
			-	BENEATH THRESHOLD
				-	SET self.wasMotionDetected = FALSE

		#	REFRESH the images STORED in the MOTIONDETECTOR
			-	ADD new CAMERA to QUEUE
			-	REMOVE oldest CAMERA from QUEUE
	#	FRAMEBUFFER1 = DEEPDREAM(FRAMEBUFFER,etc.)
		-	NET
		-	ITERATION_MAX
		-	OCTAVES
		-	OCTAVE_SCALE
		-	STEP_SIZE
		-	MODEL.end

	#	DEEPDREAM
		#	SETUPOCTAVES
			#	Framebuffer.is_new_cycle = FALSE
			#	INITIALIZE the OCTAVEARRAY with NETBLOB
			#	INITIALIZE the DETAIL BUFFER to STORE network output
			-	we can provide new values for OCTAVE_SCALE, ITERATION_MAX during SETUPOCTAVES

		#	OCTAVEARRAY CYCLE
			#	ITERATE from small to large
				-	OCTAVE is index for OCTAVEARRAY
				-	OCTAVE_CURRENT is framebuffer for each OCTAVE
				-	RESAMPLE DETAIL to mat ch shape of OCTAVE_CURRENT
					-	DETAIL comes from SETUPOCTAVES or previous OCTAVEARRAY CYCLE
				-	RESIZE the NETBLOB
				-	ADD DETAILS + OCTAVE_CURRENT to NETBLOB

				#	OCTAVECYCLE
					-	WHILE STEPCOUNT < ITERATION_MAX
						-	PROCESS the CAMERAS STORED in the MOTIONDETECTOR
						-	WasMotionDetected ?
							-	BREAK out of OCTAVECYCLE 

						#	MAKESTEP (model, OBJECTIVE, step parameters)
							-	parameters arrive here from initial deepdream function call
							-	makestep operates upon the neural net's data blob
							-	we can affect guide image and step size here (per iteration)
							-	NETFORWARD to OBJECTIVE
							-	NETBACKWARD
							-	APPLY gradient ascent step to NETBLOB
							#	POSTPROCESS NETBLOB
								-	dat gaussian blur
								-	

						-	CONVERT NETBLOB to RGB and WRITE to FRAMEBUFFER1
						-	SEND FRAMEBUFFER1 to Viewport
						-	OCTAVE_CURRENT ++

				#	EARLYEXIT
					#	LASTOCTAVE
						-	OCTAVEARRAY CYCLE reached OCTAVE_CUTOFF
						-	SET Framebuffer.is_dreamy = TRUE
						-	CONVERT NETBLOB to RGB and STORE as EARLY_EXIT
						-	Return EARLY_EXIT

					#	MOTION WAS DETECTED
						-	SET Framebuffer.is_dreamy = FALSE
						-	CONVERT NETBLOB to RGB and WRITE to framebuffer2
						-	Return CAMERA

				#	WRAPUP OCTAVECYCLE
					-	STORE the DETAILS produced during OCTAVECYCLE
					-

			#	WRAPUP OCTAVEARRAYCYCLE
				-	SET Framebuffer.is_dreamy = TRUE
				-	CONVERT NETBLOB to RGB and STORE as FINISHED
				-	Return FINISHED


#	FRAMEBUFFER

------------------------------
What is the COMPOSER?
	NumPy array with shape (height,width,RGB)		
	Always contains RGB image data
	Stores Game Loop SOURCES prior to display
		-	Deep Dream
		-	Motion Detector
		-	Overlays
			-	HUD
			-	Alerts
	Processes Game Loop SOURCES into OUTPUTS
		-	compositing
		-	resizing
	Flexibility
		-	SOURCES in the COMPOSER can be any size
			-	SOURCES in the COMPOSER are resized to the COMPOSITE W,H when composited
		-	OUTPUTS from the COMPOSER are resized to the VIEWPORT W,H

------------------------------
What is the VIEWPORT
	An OpenCV window we created to draw on the screen
	An Event Listener for external input
		-	listens for keyboard events every frame
	Flexibility
		-	window can be drawn at any size
		-	supports multiple windows
			-	all windows use the same event listener
		-	provides PREPROCESS inserts
			-	color transform
		-	provides POSTPROCESS inserts
			-	HUD overlay
			-	ALERT overlay



currently,
we almost always write directly to buffer1
-	camera image
	-	fetch camera before entering game loop
	-	return value from deepdream when motion detected during OCTAVECYCLE

-	computed image
	-	initialized with zeros at startup
	-	REM cycle
		-	deepdream return value after non-interrupted REM CYCLE
		-	running inceptionxform (on self) after non-interrupted REM CYCLE
	-	Interrupted REM cycle
			-	composited with buffer2 at beginning of new REM CYCLE if previous cycle was interrupted
	-	OCTAVE CYCLE
		-	neural output from each non-interrupted iteration of OCTAVECYCLE
		-	composited with buffer2 after interrupted OCTAVE CYCLE (is it?)


we sometimes write directly to buffer2
-	initialized with zeros at startup
-	motion was detected during the OCTAVECYCLE
	-	buffer2 stores the last hallucinated frame
	-	deepdream exits and returns camera
	-	buffer1 stores deepdream return value (camera)

2016-11-07 17:03:13
-	Tracking
	-	automate tracking thresholds
	-	trigger events based on "hot" areas of the screen
		-	screen edges?
		-	the cell of an n x n grid with the brightest value?

-	dynamics
	-	cleanup the "programs" currently in use to allow switching between them
	-	cleanup color processing on viewport
	-	add support for automated events

-	display
	-	keep a buffer of final output data (history buffer)
	-	playback history buffer
	-	composite / replace live with history
	-	global frame blending (as in after effects)
		-	 no longer special case new camera image acquisition
		-	 all frames are averaged together before display

-	HUD cleanup
	-	image export
	-	twitter post on demand (?)

AUTOMATE TRACKING THRESHOLDS
every time I set up a session, I have to double check the threshold and lower it or raise it so that motion is detected at a known degree of sensitivity.

if subjects are close to the camera, all the counted values increase

AUTOMATED EVENTS
-	different kind of transforms on REM cycle
	-	scale vertical vs. cale vertical + h, anchor left
	-	value of scale variable
		-	random?
		-	sequenced?
		-	cycle?
		-	related to number of pixels counted during motion detection?
	-	blur multiplier
	-	different feature maps on a given layer

BEST LAYERS
inception_4d_5x5_reduce

2016-11-07 18:06:56
theres a bug with the viewp[ort scaling - its scaling from upper left anchor instead of center anchor

2016-11-07 23:20:57
a more efficient way to resample the viewport?

2016-11-08 01:32:23
added feature map selector to make_step() wow...

2016-11-08 14:45:10
taking a second look at feature map rendering style
priority for this work session is to get tracking automated
better metrics on HUD
fix viewport scaling to work from center instead of top left edge

username
settings
threshold
last
now

2016-11-08 15:40:51
CREATE AN INVENTORY OF EFFECTS. BE ABLE TO SWITCH BETWEEN THEM

for what I'm looking at right now I want to specify:
-	Model
	-	Layer Index
	-	Feature Index
-	Deepdream basic parameters
	-	Iterations
	-	Octaves
	-	Octave cutoff
	-	Octave scale
	-	Step Size
	-	Step Size multiplier
-	Renderer
	-	Make_Step()
	-	Make_Step_Feature_Map()
	-	REM cycle flag (TRUE/FALSE)
		-	TRUE (current value, hallucinate until new camera input)
		-	FALSE (stop processing until new camera input)
-	Modifiers
	-	Feature Index incrementor
	-	Layer Index incrementor
	-	Octave Scale
	-	Pause Motion Detection
	-	REM Transform scale
	-	REM Transform center point

2016-11-08 22:47:32
about to start work on automated tracking. I think that collecting the last n samples of the delta_count then calculating a moving average from that to select the threshold i sthe right place to start

x check the full range of display resolutions available for camera

2. draw stats on screen as needed

3. represent delta count as % is the value the same independent of capture size ?

2016-11-09 02:45:47
I've made the motion detection threshold dynamic - the raw delta count values are placed in fifo queue with fixed length, the queue values are averaged with each step. the threshold value is set to that. Its effective

2016-11-09 03:09:32
working very well, cool feature - still needs a bit of refinement - but playing with some tweaks makes it easier to bias the averaged value. Having them values as history is also cool - the way to deal with closeups is to attenuate large value differences, which should stand out in the sampled delta counts

2016-11-09 10:14:51
if the detector history window width is 2 then its just averaging the last 2 values?

2016-11-09 10:26:52
camera dimensions
# max 2304 x 1536
# 1920 x 1080
# 1600 x 896
# 1280 x 720
# 960 x 720
# 864 x 480
# 800 x 600
# 640 x 480
# 352 x 288
# 320 x 240
# 320 x 180

2016-11-09 11:33:48
maybe there is another way to calculate moton detection?

2016-11-09 12:09:00
maybe. need to move on to other things though. the current method is an improvement

2016-11-09 12:58:45
lookimg so Dark when webcm contrast/exposure is made sorta noir

2016-11-09 15:26:49
Looking at creating "programs" that I can switch between

2016-11-09 16:21:43
how do I "switch" programs now?
Amplifier.set_package('ghost')

what if I could keybind that behavior and switch between?

what is a "program"?
what is the difference between program A and program B?

# 1
A: begins at inception_4d/5x5_reduce
B: begins at inception_5a/5x5_reduce

# 2
A: octave_scale = 1.8
B: octave_scale = 1.2

# 3
A:	uses make_step_featuremap
B:	uses make_step

# 4
A: static mode
B: REM mode

# 5
A: uses 'places' model
B: uses 'cars' model

# 6
A: starts at featuremap[1,2,3,4,5] index 0
B: starts at featuremap[5,10,15] index 2

2016-11-09 20:15:10
moved event listener out of Viewport class is now a global function

2016-11-09 20:24:21
passing the listener function to Viewport instance

2016-11-10 09:36:59
changing layers forces new cycle now, implementing same for featuremaps

2016-11-10 12:03:55
verifying feature map incrementor setup

2016-11-10 12:12:14
works. doing some cleanup before commiting

2016-11-10 15:45:02
modifying the program data definitions

2016-11-10 17:50:12
remaining
x	fix pause functionality
-	work out how to switch programs with program select
x	exporting stills
-	create programs and test

2016-11-10 19:12:55
fixed pause functionality - much less convoluted than previous implement

2016-11-10 21:19:50
assigning layers to those specified in a program's layer list

2016-11-10 23:17:59
pulling layer list from program definitions now

2016-11-10 23:35:53
pulling featuremap list from program definitions now

2016-11-11 08:18:26
Setup 1p at Hotel Zetta. Take the next hour to look at switching network models with progam

2016-11-11 09:32:07
autosaving fully composited frames at end of cycle. still need ability to save on demand

2016-11-11 09:50:37
forced refresh will save the return value from deepdream early exit - this will be a clean camera image. Saving on demand also implemented - this saves whatever is in the image buffer - scaled up to dimensions of viewport.
clean saves of high res material are guaranteed only when a cycle is completed - and that saving is automated

2016-11-11 09:53:05
-	work out how to switch programs with program select
-	create programs and test

2016-11-11 10:50:01
modifying program list data structure

2016-11-11 11:10:21
wtf did that code work the first time through :) :) :)

2016-11-11 11:21:08
adding some error handling to prevent crash when featuremap index goes out of range for a particular layer

2016-11-11 11:24:07
now isnt really the time for that... revisit iof possible

2016-11-11 11:30:46
fixed the problem at featuremap selection

2016-11-11 11:39:46
basic program selection working - need to flesh out further

2016-11-11 12:41:05
model parameters not updating when I switch programs - may need to abandon that idea for now

2016-11-11 12:47:43
simple fix. working now.
give yourself 30 calm minutes to find some cool settings
add more from the location

Turning up the silence in Sci-Fi city at @codame artificial experience show


2017-03-12 15:53:49
rethinking some ideas for the L.A.S.T Festival exhibit


2017-03-14 14:59:45
Its working again, but had to wipe everything. The program was behaving strangely on this new machine. Described above. Despite dreading it, I reinstalled Linux and then the deep learning dev environment. Refined the notes I've been keeping on this. Maybe some new advantages. OpenCV is now at v3.2. I compiled it with option to do linear algebra with Cuda library. It seems faster. but hard to say definitively


2017-03-14 15:43:07
GOALS
CODELOCK
HARDWARE
INSTALLATION
UNINSTALLATION


2017-03-18 17:13:39
I've sourced a mobile AV cart w some accessories and will be placing that order shortly.


2017-03-18 17:36:16
can i make it show only fully rendered frames?
well first of all, lets review how it works



2017-03-19 14:44:13
I have the camera transform working in a test project
probably 
overthinking.
the goal:
rotate the camera input upon reading it

is this a matter of:
1. creating a wrapper function to extend cv2.VideoCapture.read()
2. decorating the existing function?

2017-03-19 15:06:02
motion detection runs in portrait now


2017-03-19 21:23:50
getting close. its a bit of a hack.


2017-03-19 21:33:03
hardcoded portrait orientation is working

NEXT STEPS
- study python function decorators
- cleanup camera orientation functionality
	- choose between portrait and landscape at launch
- examine frame export
	- what's it currently doing?
- investigate the functionality of a Memory class
	- stores rendered output in RAM as an array
	- playback rendered output to framebuffer
- guide images
- switch between 2 cameras
	- camera 1 faces faces the viewer and acts as a mirror
	- camera 2 is behind the screen and acts as a window


2017-03-21 21:34:43
I reimplemented the camera capture system as a threaded queue after a bit of sould searching. Not sure what I was expecting to see. Something? Nothing? Is the system behaving more smoothly now? I can't actually tell. Seems largely the same. How would I be able to tell?
Is there a way for me to profile the systems performance?
- avg. iteration time
- octaves/sec
- current calculation time
- last cycle time


2017-03-21 21:37:58
Is the motion capture not threaded enough? should all of that be happening on a seperate thread? what would be the benefit?
Instead, could it happen on a seperate process?
What if the deepdream computation was happening on a different thread instead, and the output was being queued so that
deepdream.read() would return the next frame in the queue? how woyuld this change the approach to frame buffering?


Python threading doesn't multiprocess - it just makes more efficient use of the CPU
What about the rpyc stuff I'd previously looked at?
The idea is that motion detection and deep dreaming happen in seperate processes
The expected benefit:
computation happens in queues and results fill up a bin
Asynchronous
- decouples display rate from computation rate
display pulls the next available frame from a bin and shows it
may be possible to compute upon bin1.read() + bin2.read()


2017-03-21 23:14:29
looking at rpyc
reading up on python multiprocessing, which offers similar API as Threading

The multiprocessing module comes with plenty of built-in options for building a parallel application. But the three most basic (and safest) are the Process, Queue and Lock classes. 

PROCESS
The Process is an abstraction that sets up another (Python) process, provides it code to run and a way for the parent application to control execution.

from multiprocessing import Process

def say_hello(name='world'):
    print "Hello, %s" % name

p = Process(target=say_hello)
p.start()
p.join()

QUEUES

Queue objects are exactly what they sound like: a thread/process safe, FIFO data structure. They can store any Python object (though simple ones are best) and are extremely useful for sharing data between processes. Queues are especially useful when passed as a parameter to a Process' target function to enable the Process to consume (or return) data.

from multiprocessing import Queue

q = Queue()

q.put('Why hello there!')
q.put(['a', 1, {'b': 'c'}])

q.get() # Returns 'Why hello there!'
q.get() # Returns ['a', 1, {'b': 'c'}]
q.get() # waits for more data to pass through the queue

LOCKS

Like Queue objects, Locks are relatively straightforward. They allow your code to claim the lock, blocking other processes from executing similar code until the process has completed and release the lock. 


2017-03-22 08:29:11
looking at the test application,significant speedups are possible, but how can I apply these ideas to deepdreamvisionquest?
QUEUES:
	next camera frame
	next deepdream render
	next displayed frame

* is it possible to retrieve data from the queue that has already been read? is it random access, or is it sequential by definition?

I'm assuming that queung this information lets me address it asynchronously. For example, show the deepdream rendered que once every second


2017-03-22 08:47:04
who are the workers?

the deepdream function
the capture function

the compose/viewport functio


2017-03-22 19:50:21
I came across some code samples showing a single threaded, multithreaded and multiprocess approach to structuring code. I'm becnhmarking those approaches to see what they do

range: 1,10000,1

SINGLE THREADED
runtime: 50.6829841137s
CPU load during run: 0.96
1 core is in 100% usage throughout

MULTITHREADED 
runtime: 83.9671368599s
2.10
all cores are approx 19-30% in use
* note that this 

MULTIPROCESSOR
runtime: 72.0738749504s
2.05
all cores are approx 30-40% in use
* note that this 

these results are unexpected. taking out the print statements and remeasuring
ending some processes to get a cleaner benchmark

10000, 100000, 100

SINGLE THREADED
runtime: 86.0674118996s

MULTITHREADED (4 threads)
runtime: 89.8049190044s


MULTITHREADED (8 threads)
runtime: 96.2501211166s


MULTITHREADED (16 threads)
runtime: 106.664397955s


MULTIPROCESS (4 processes)
runtime: 88.1409959793s

MULTIPROCESS (12 processes)
runtime: 88.1409959793s


2017-03-22 21:11:22
No room to investigate this much further beyond tonight.My fundamental premise is the right one - decouple computation from display, but implementation is too expensive


2017-03-22 21:23:25
trying one more exercise - slightly different method



2017-03-23 00:47:04
pulled myself away from the optimization experiments and started looking at image processing.
there's a difference between using nd.filters and cv2.filters
getting significantly wider blur fx with some new methods


2017-03-23 00:52:21
ending worksession - frustrating and rewarding at once. there's so much I dont know


2017-03-23 19:01:48
doing some remedial work on numpy before starting this image processing worksession


2017-03-23 21:17:43
wrapped up the remedial work. took a closer look at numpy arrays and matplotlib


2017-03-23 21:18:32
so moving forward - how would I subtract from the output red channel each frame, checking to see if it was 0


2017-03-25 01:05:29
figured out the crash that turned up during last session - or at least figured out how to avoid it. When the number of max iterations is reduced, less time is spent computing. It seems that if the same image is passed to the network at a high enough rate, it crashes. No idea why. Its arcane. Anyway, by scaling the recycled input with a multiplier > 0 the problem doesnt turn up.

More sigfnificantly, I made some exciting progfess towards a more expressive visual language. I costs nothing to color correct and transform the output after its been computed. I'be also tweaked a number of the deepdream make_step parameters. not sure what will stay, still experimenting.

The danger is to get caught in a loop of experimentation though.
1. how can I save the settings and configurations I come across so I can find them again?
2. camera 2
3. what are the controls exposed to participants
4. program USB pad w ASCII sequenceas for controls


2017-03-25 10:28:52
goals (Saturday)
- transforming during the cycle
	- is possibnle? how?
- color correction beta
	-	color
	-	luminance
- image transformation beta
	-	scaling (zooming in)
	-	warping the frame buffer

goals (Sunday)
-	dual cameras
-	guide images


2017-03-25 10:38:44
studying image translation

translation basically means that we are shifting the image by adding/subtracting the X and Y coordinates. In order to do this, we need to create a transformation matrix,

rotation matrix
We can specify the point around which the image would be rotated, the angle of rotation in degrees, and a scaling factor for the image


2017-03-25 18:52:56

reading about 2D convolution (in regard to image processing)

What does "frequency" mean in an image? Well, in this context, frequency refers to the rate of change of pixel values. So we can say that the sharp edges would be high frequency content because the pixel values change rapidly in that region. Going by that logic, plain areas would be low frequency content. Going by this definition, a low pass filter would try to smoothen the edges.


2017-03-25 20:39:01
came across a section on how to make a vignette.
this is probbaly something that should happen at the post rendering stage, similar to the HUD


2017-03-25 21:54:54
came across method for gamma correction


2017-03-25 22:52:24
I've been able to get a kind of color grading happening with what I've learned today. The code is sluggish at the moment as not of what I've added is optimized, and in particular  the vignette that I'm adding is sort of expensive. Also not sure if gamma correction on the input or the output or both is the way to go. I have the computation setup on the camera input, but again, pretty wasteful - is calculating the lookuptable every frame, when it only needs to do so on init and when the gamma value changes.

I'll want to add a control for increasing/decreasing gamma. Interesting to see how it reacts to exposure and brightness set on the Linux camera control utility


2017-03-26 10:08:30
turned off the color grading functionality created yesterday until I can optimize a bit further. 
goals:
	- integrate camera 2
		- realtime switching between cameras
		- composite views
			- overlay
			- 2-up
		- just had an odd idea - is it possible or desirable to create a small snapsot of the camera and composite that on to the viewposrt so that, multiple frames are always shown.
			- further, it would behave liek the queue I'd been thinking about, the most recent capture would always be shown as the last image, and would push older images out of the stack.


2017-03-26 10:12:25
easy enough to access the different cameras by indes. a good start :)
- add a keybind to switch between cameras at runtime


2017-03-26 11:16:41
Just ran it with 2 cameras simultaneously at 1280 x 720. Not wuite sure what the expense was. System seemed responsive - perhaps a bit less fluid than before?


2017-03-26 13:15:01
I'm wanting to replace all the print statements w proper logging

The different levels of logging, from highest urgency to lowest urgency, are:

CRITICAL
ERROR
WARNING
INFO
DEBUG
The setLevel() call sets the minimum log level of messages it actually logs. So if you fh.setLevel(logging.ERROR), then WARNING, INFO, and DEBUG log messages will not be written to the log file (since fh is the log handler for the log file, as opposed to ch which is the handler for the console screen.)

To write a log message in one of these five levels, use the following functions:

logger.critical('This is a critical message.')
logger.error('This is an error message.')
logger.warning('This is a warning message.')
logger.info('This is an informative message.')
logger.debug('This is a low-level debug message.')


2017-03-26 14:00:54
there's a lot more to logging than expected, but I've got a good replacement for all those print statements, now - back to work on that camera!


2017-03-26 14:50:46
realizing that yesterdays tests that I thought were running on a 1920 x 1080 input were actually running on a 1280 x 720 input and scaling up to 1920 (which looked great actually). Those values were hardcoded into the camera instance


2017-03-26 14:52:18
crashes when I set portrait_alignment = False. but why?


2017-03-26 20:23:43
reverted back to the point before I added logging, will continue with print statements as before.


2017-03-26 22:56:58
getting there - able to toggle portrait_alignment without crashing


2017-03-27 11:49:30
struggling with the viewport.
Here's the problem.

I want to be able to toggle portrait_alignment on/off
why?
so that the viewport shapes itself to match whatever the camera is outputting


2017-03-27 17:49:33
making some progress wi the viewport finally


2017-03-27 22:04:44
It seems that the Composer.buffer array needs to be reshaped as well
Hunting this down is so much harder than it needs to be. It points out the fallacy of decentralizing these sources.


2017-03-27 22:11:59
Here's the reality. you need to move on. Forget about the idea of generalizing the camera orientation. Just assume it to be oriented properly when the program starts. It doesn't need to switch back and forth at run time.

With that in mind - I can do something like this:

create camera objects
derive viewport size from camera.width,height
de


2017-03-27 22:37:19

typed in a bunch of stuff maybe it works. 
basic idea was to pull capture_size from the camera object
Viewpoert_size has become an instance of the class Display, which exists at the moment only to house a width and height value accessible thrui dot notation. Once I get it working, I'll replace that bit with a dictionary, or movit back to the Data module.

mocing on, I made global substitutions to reference these changes. At a minimum it shpuld crash in the same way as before.


2017-03-27 23:18:28
its hallucinating on either camera in landscape again
and crashes on portrait just as before - same reasons 


2017-03-27 23:40:22
a bit more detail has it crashing further along. This time it showed the camera output in portrait orientation before crashing. Now that the display size is being adjusted when initialized, the previous conditions I wrote there no lobger applies


2017-03-27 23:43:22
There we go - its working.
I can switch between portraint and landscape modes when the program initializes

Let me try to sum up:

The Display is the onscreen framebuffer.
The display supports 2 aspect ratios:
-	landscape (16:9) default
-	portrait (9:16) transposed counter clockwise
-	the display can be flipped horizontally and vertically in any aspect

The Camera is the framegrabbing and Queing system

Create a camera object, specifying:
- capture_width,
- capture_height
- portrait_alignment 

The Display object relies upon the camera object 
-	display width, height are stored here
-	display width, height are swapped here to match the camera alignment
	-	if the orientation is portrait then the specified display width and height have to be swapped
- the Viewport class relies on knowing the proper Display width, height so:
	- Viewport.show() can scale lower ocataves in buffer1 proportionally to match the display size
- the Composer class relies on knowing the proper Display width and height so:
	- Composer.update() can run inceptionxform on buffer 1
	- buffer2 can resize itself to match the Display width
- show_HUD() relies on knowing the proper Display width, height so:
	-	the function draws HUD updates to a seperate frame buffer that needs to match the DIsplay size

/* I'm noticing that Viewport.show() and Composer.writeBuffer2 basically do the same thing
Viewport.Show() is actually writeBuffer1() + show() */


2017-03-28 00:57:33
cleaned up the logging (print statements) - got rid of most of it
The camera/display issue isnt fully resolved, the frame buffer isnt calling the inceptionxform properly, so it just sits on the same image


2017-03-28 13:28:56
Added expandable logging framework to debug the code better and I guess also as a bit of a programming exercise. Was not happy with my  progress yesterday, enough so that I took a day off from work  to  get my momentum back


2017-03-28 14:56:16
replaced all print statements with logging calls. In a much better position to debug efficiently.


2017-03-28 22:28:52
I have the system up and running on the Monolith. It looks startling. Its amazing. Numerous conclusions to be drawn from the initial test run:
-	the video4Linux Control Panel is only addressing a single camera. Is there a way to run 2 instances of this program and specify the camera?
	- as a fallback, is it possible to emulate aspects of the control panel in software?


2017-03-29 00:34:41
Yes, there is a way to run 2 instances of the video4Linux control panel. There's a lot more functionality there than I knew. It also turns out to be trivial to mirror the captured image vertically and horizontally. Vertical mirroring is surprisingly cool, the forms that emerge are a bit disconnected from your movements.

I'm going to implement camera switching next and then camera flipping
Before getting to that, there's a rendering bug where:
x the sine wave transform doesn't get picked up by the next rendered image, so it appears briefly then disappears instead of propogating
x the octave size frequency mod isn't working
x the inceptionxform funtion isn't calculating the transform correctly


2017-03-29 20:52:59
x	camera switching by pressing F1 / F2
P1 	refine motion detect to allow getting close
P1	sequencing - motion between programs
P1	parameters - what are they - create a list
P2	saving good values - how?
P2	guide images
P3	image capture


2017-03-29 21:18:56
HUD is back online. making the text smaller
am also wondering if possible to output those values to a MatPlotLib window?


2017-03-30 01:19:27
both cameras are running simultaneously. I'm not seeing any real slowdown or latency as a result


2017-03-30 10:24:24
camera switching is working and its cooler than I thought it would be - except for the initial switch, which seems to rely on motyion being detected instead of the viewport being forced to refresh


2017-03-30 11:07:31
camera switching looks like its working - have not fully tested motion detection. looking at that next


2017-03-30 22:26:37
some problems re-addressing camera by index when I switched the USB ports prior to rebooting. Still trying to remember how I brought up the control panels for the cameras

2017-03-31 00:05:32
P1 	refine motion detect to allow getting close
P1	sequencing - motion between programs
P1	parameters - what are they - create a list
P2	saving good values - how?
P2	guide images
P3	image capture
P2	duration based time-out from dreams
	-	forces end of cycle based on how long its been running
P1	transition from end of cycle to beginning of next so the progression is not quite so abrupt


2017-03-31 13:47:00
taking a look at MatplotLib for analyzing what the motion detector is doing .
Keep in mind that there are 2 other areas needing momentum.
P1 	refine motion detect to allow getting close
P1	sequencing - motion between programs
P1	parameters - what are they - create a list



2017-03-31 15:03:21
I found some code to do realtime plotting w matplotlib, looking at it running now. Is pretty CPU intensive. 


2017-03-31 23:18:05
added support for flipping camera input horizontally or vertically


2017-03-31 23:20:49
taking a second look at gamma cprrection


2017-04-01 02:38:11
I put some rough  monitoring in place on teh motion detection viewer, but all it showed me was that the behavior is  more fluid and complicated than I thought. The previous concept of an "overflow" when the current sample and next sample are both over the threshold, doesn't seem to happen any more becaus the threshold is raised by the average value of the last 50 samples

or something like that. In any case its hard to quantify the conditions that result from large motions near the camera. To solve this problem further, I need to look at the data that gets generated.

For tomorrow - put this aside, and work on program settings
- need an explorer setting (which allows me to navigate the space)
- need a way to toggle back and forthe between explorer mode and automated mode
	+  for demonstration
	+  for identifying settings
- need categories for program settings
- need a timer to switch between programs
- need a way to switch network models from within a program
	+ what else needs to be captured within a program?
		* brightness cycle


2017-04-01 14:27:41
reading up on file handling in preparation for saving out program settings.

WHAT ARE PROGRAM SETTINGS?

Currently:

	name:
	iterations:
	step_size:
	octaves:
	octave_cutoff:
	octave_scale:
	iteration_mult:
	step_mult:
	model:
	layers: []
	features: []

new parameters:
capturefx: [] 	# ordered list of image processors called each capture
stepfx: [] 		# ordered list of image processors called each step
cyclefx: [] 	# ordered list of image processors called each cycle


2017-04-01 17:09:30
status:
I've created an FX class
inside are 2 functions - xformarray and octave_scaler
I'm instantiating an FX object  and manipulating that
currently as explicit commands:
FX.xform_array(Composer.buffer1)
FX.octave_scaler(model=Model)

how would I pass these in from a list, or dictionary?

# xform_array, Composer, octave_scaler, Model are all global references available to the FX class
cyclefx = []
cyclefx.append({
	which_func: xform_array,
	which_params: Composer.buffer1
})
cyclefx.append({
	which_func: octave_scaler,
	which_params: Model
})







FX = FX(composer=Composer, model=Model, fxlist={function1, function2} )

class FX(object):
    def __init__(self, composer, model, fxlist):
    	self.composer = composer
    	self.model = model
    	self.fxlist = fxlist
        self.direction = 1

        cyclefx = []
        cyclefx.append({
        	which_func: xform_array,
        	which_params: [Composer.buffer1, 10]
        })
        cyclefx.append({
        	which_func: octave_scaler,
        	which_params: [self.model, 0.1, [1.2, 1.6]]
        })

    def process(self):
    '''
	iterate thru the functions in fxlist here. where do the parameters come from?
	1. xform_array needs:
		- reference to relevant image, assumed to be from Composer.buffer1
		- multiplier value for step function

	2. octave_scaler needs:
		- pointer to Model where the deep dream params are stored
		- scaling factor
		- upper and lower limits
    '''
[self.composer.buffer1, shift_amount]
[self.model, scaling_factor,[1.2,1.6]]
FX.process(cyclefx)


2017-04-01 23:04:48
taking a different approach after some futher thought. Added a cyclefx dictionary containing pointers to functions within an existing program dictionary. Its working as expected. Experimenting with placement of the funtions that get dispatched. These functions are cufrrently defined in the same Data module as the program definitions themselves.


2017-04-02 00:02:37
closer to working now. successfully calling the function specified if the program with the arguments specified. Messy looking. Seeing where I can cleanup.


2017-04-02 01:39:15
cleaned up the data structure of the program a bit so that the fx block is structures like this:

'cyclefx':[
	{
		'func': function1,
		'params': {'param1':'dogs', 'param2':99}
	},

	{
		'func': function2,
		'params': [1,2,3,4]
	}
]

cyclefx is a list containing dictionaries which store function pointers and parameters to be called upon with each cycle

fxlist = Model.program[Model.current_program]['cyclefx']
do_fx = fxlist[index]['func']
params = fxlist['params']
do_fx(**params)


2017-04-02 10:03:22
This syntax is so tortured, it can't be right, but uit's working.  Needing excpert advice (Spoto?)  to take a look through this.  What I'm doing feels well intentioned, but is so messy it must be a haCK?


2017-04-02 10:07:23
Those parameters could come from anywhere, and might superficially cleanup the code to do som, but doesn't make sense that the function parameters would be seperated from the function pointers


2017-04-02 15:17:10
note to self before I forget. Anyone who's ever wanted to "learn to code" needs to experience this moment to truly get it. The stakes seem so high to me right now, and looking backl I've put so much of myslef into understandingthis idea and how to realize it. Learning python has been a big part of that. I didn't realize how beautiful the language is. Truly, its like Elvish. But right now - thinking through the trial and error of passing functions and parameters as part of a "program" that drives my artwork is the most challenging computer science ever. Its bitter to know that you could have done it differently, that you didnt understand something the way you thought, or that  you are almost certainly missing out on a basic concept, knowledge of which would make this current impasse invisible. Still - I'm hacking my waty to the solution, and its happening right now!


2017-04-02 15:57:00
Fantastic - just demonstrated solution to storing functions and function parameters in pre-programmed definitions


2017-04-02 17:41:33
Still not there. What if I'd been making the wrong assumptions entirely. The functions in question could be  written to the Model class, just like the rest of the current mocel parameters, such as step)size and so forth.


2017-04-02 18:18:49
working implementation now. Demonstrated switching between 2 different programs with different params for the xform_array cyclefx.
x implement same for octave scaler
x iterate thru the list stored in Model.cyclefx
- implement feature for stepfx


2017-04-02 21:24:32
until now it wasn't really obvious to me that a higher octave_scale led to a faster cycle time. not just by a little, either


2017-04-02 21:40:17
Fantastic news! its working as designed. NMot quite the way I thought it would, but ended up cleaner than prior work sessions suggested. A smuch as I want to pass in a "job list" of functions to each of these programs, I don't know how to setup the system to make that happen. The problem is that the Program data structure is just attached to its module luike a filing system. Its difficult to reach into and pass pointers to dynamic quantities, such as Composer.buffer1. I found it difficultr to do while also passing in specific values - parameters that I wanted top pass to a function, such as blur=3

Maybe after a day and half of hacking it, if I were to readress the probglem, I'd know how to solve it better. Already some ideas, such as turning the Program data structure into its own class. Not sure why I previously didn't.


2017-04-02 22:50:44
adding stepfx now


2017-04-03 00:35:17
added inception_xform to cyclefx list
cleaned up program deginitions somewhat


2017-04-03 01:47:34
added median filter and an opacity function to stepfx. Median Blur behaving oddly though, disallowing kernel sizes > 5 Otherwise working as expedted

- bilateral filter
- gaussian filter
- duration_cutoff (early exit to rem cycle based on timer)

[not sure if these are stepfx or cyclefx]
P1 program switcher (chooses another program based on timer)

P1 Vision Quest
	- explore program settings
	- write out textfile w current settings on demand 

P! Controls
	- new keybindings
		+ Toggle Camera
		+ Reset to default program
	- verify functionality w external USB keypad
		+  can Thea help with key labels?

P1 Exporting Images & Video


2017-04-03 18:31:44
added bilateral filter to stepfx list
x bilateral filter
x gaussian filter
x duration_cutoff (early exit to rem cycle based on timer)


2017-04-03 19:28:45
How does the duration cutoff stepfx work?
- specify a duration
- make note of the time when each cycle starts
	+ where?
		* The FX object?
- with each call to the duration_cutoff() function, get the elapsed time by subtracting the current time from the start time
- if the elapsed time is greater than the specified duration then
	+ how to force a new cycle to start?
		* force MotionDetector.wasMotionDetected = True ???
		* use the descriptively named Viewport.force_refresh flag?
			- yes, this. I created a refresh() function to wrap that

2017-04-03 21:32:53
I have the basic timer function setup, and verified registering time on the FX.cycle_start_time property each cycle. It's getting the data passed to it from the program declatration as well.


2017-04-03 21:43:43
The cutoff function is working and can also be used as the basis for the program timer, but its's rough. calling Viewport.refresh() immediately refreshes the viewport, but would be much more fluid if the new cycle and the old dissolved - exactly the way it happens during motion detection and Composer.is_compositing_enabled = True. SO how does that work?


2017-04-03 22:04:37
the transitional behavior I'm describing takes place during the normal course of things when
	- we've entered a new cycle, AND the MotionDetector is NOT in a 'resting' state
	- what does 'resting' mean? just that the readings have stabilized enough that the current reading matches the previous reading
		+ so when the MotionDetector isn't resting it just means that the current value was different than the previous one. Which must happen often enough.
		+ From what I can tell, the resting state can only refer to a condition where there is stillness (of course). 
			* the  pixel count values must be zero or beneath the floor, , and so are reported as zero.
		- this period of stillness corresponds to the hallucinating state -. In other words, 'it can only see you when you're moving'

2017-04-03 22:58:30
did a bit of invetigation into how motion detection works. Calculating a "ratio" based on pixels_detected/total_pixels. This shows a percentage of how much of the screen is in motion. One of the areas I wanted to enhance was relaxing motion detection when subjects are close to the camera. This is the basis for that determination


2017-04-03 23:02:33
The reason I'm getting an immediate "cut" instead of a dissolve for the duration_cutoff function is because I'm only refreshing the Viewport to force a new cycle. I also need to override the MotionDetection resting state.


2017-04-03 23:13:57
That worked. FInished implementing the duration_cutoff stepfx. Playing around with it , I;m not sure how much value it has. Its definitely a different experience. It feels closer to realtime, especially when the duration is set low,  which effectively delivers a consistent (although low) frame rate. Thing is, the images generated are incomplete and in some case, pretty low resolution. Maybe not si attractive. Will have to test this feature out to see the valdity.


2017-04-03 23:16:20
Picking up work on the Sequencer control next. This is a stepfx almost identical to duration_cutoff.

What does the sequencer need to know?
- index of next program
- time remaining until start next program

Does the sequencer need to be specified in program declaration?
- no

Where is the program duration stored?
- let's assume that all program's run for the same durayion
- when a program starts, it registers its start time in the FX class
- actually, no - its more self contained if all that info is kept in the Model class, with all the other program params

- specify a duration
	+ where?
		* attached to each program?
		* specified by the function call (so all programs are of the same duration)
- make note of the time when each program starts
	+ where?
		* The FX object
- with each call to the sequencer() function, get the elapsed time by subtracting the current time from the start time
- if the elapsed time is greater than the specified duration then
	+ select another program
		* how?
			- step thru program list indices, just like prev/next controls already do
			- 
		* force MotionDetector.wasMotionDetected = True ???
		* use the descriptively named Viewport.force_refresh flag?
			- yes, this. I created a refresh() function to wrap that

-

2017-04-03 23:41:46
removed Viewport.refresh() from the duration_cutoff() function. Its more interesting now that it doesn't re-do the whole screen.


2017-04-04 07:23:04
implemented basic program sequencer. It just cycles through the program list by calling Model.next_program() 
- what about "themed" programs? For example, "afternoon" and "evening"?
The program list is 1 dimensional at the moment, but could do something like this:

program = {
	
}

program = [1,2,3,4]
kb
program = [
	[1,2,3,4],
	[1,2,3,4]
]

This would be the basic structure allowing  me to access programs banks
program = {
	'am': [1,2,3,4],
	'pm': [1,2,3,4]
}

This is how the program declaration would look
program['am'].append({
	'name':'geo',
	'iterations':10,
	'step_size':3.0,
	'octaves':4,
	'octave_cutoff':4,
	'octave_scale':1.4,
	'iteration_mult':0.5,
	'step_mult':0.0,
	'model':'places',
	'layers':[
		'inception_3b/5x5',
	],
	'features':[-1,0,1],
	'cyclefx':cyclefx_default,
	'stepfx':stepfx_default
})


2017-04-05 00:06:19
Programmed the USB keypad with some keyboad macros and am validating on Linux


2017-04-05 00:30:13
I've validated the input from the USB keypad. It works! Need to change a few function assignments to match though.
- Toggle Camera
- Reset All
- Prev/Next Program Bank
- stub in listener definitions for unassigned keys

Think about the kind of logging that is most useful in realtime - in the terminal
Motion detection status:
floor
delta_threshold
current value
Ratio
program change
layer change
featuremap change

How are images being saved?
Have you tried the other network model? Is it possible to switch between them  in a program? What happens when you try?


2017-04-05 01:11:01
taking a quick look at how the network model is imported. It seems that its is assigned to the model instance with a keyvalue when the object is created.

the choose_model() function is only called when the class is initialized


2017-04-05 01:25:18
Uh... wow . Swapping the model as part of aprogram change seems to work just fine. That's great! The Model class is a bit of a mess. I knew a lot less then. What will my code look like  6 months from now?


2017-04-05 01:56:48
What's left?
P1 Implement Program Bank system
P1 Prev/Next Program Bank
P1 Pause Seqeuncer - for demoing or live exploration through  layers or featuremap without the program change interrupting
	- can create a dedicated bacnk for a program(s) that support this behavior
	- 
P1 Exporting images
	- every octave?
	- every new cycle?
	- every completed frame?
		+ is there a way to identify completed frames in the filename?
		+ Is it possible to export buffer2 as well?
P1 Create and curate programs
x Toggle Camera
	P4 what would it take to combine the camera views? Where would that be done? How?
P1 Reset All
P2 Add listener definitions for unused keys
P3 Take another look at motion detection. Is it possible to gate the detection behavior when the ratio is above a certain threshold?


2017-04-05 14:06:42
working on Toggle Camera


2017-04-05 15:22:12
reorganized listener function and logging. verified keypad input


2017-04-05 15:30:15
How do we know which camera is the current one?
Webcam.current is the index in the camera list
Webcam.get() return s a pointer to the current camera

How do we set the current camera by index?
Webcam.set(index) will return a pointer to the current camera and update the Webcam.current value


2017-04-05 16:11:23
implemented toggle camera


2017-04-05 16:27:42
testing what's working with image export before diving further into the program bank system


2017-04-05 16:38:39
getting too many chaff frames, what if I just wanted to see fully rendered frames
or what I wanted to see only composited frames?


2017-04-05 16:44:59
Best place to export frames is from the same  cyclefx case that runs inception_xform. What if  thet fx hadn't been used for a program  though? Where would rendered images appear from?


2017-04-05 16:53:16
completed export pipeline.
- add a control to enable/disable feature to finalize
- add HUD label for "exported: [filename]"

2017-04-06 00:08:18
It's close. You need to think about simplifying and finishing. Great beta test earlier this evening w Scott Storrs and Aileen. Some kind words, but more importantly - the chanc eto see how the current system behave in a public situation. Some outcomes

1. Dont expose anything but camera selection on the control panel
	Maybe also the HUD
	And pause motion detect
	The rest of the controls stay assigned to the keyboard, which is easily accessible
	Doing so requires me to repogram the USB keypad

2. Keep every program in bounds of current parameters
	Reset parameters when switching programs (pretty suire this is already happening)


2017-04-06 01:14:40
Disabled image export for the moment. Dont forget to re-enable it


2017-04-06 01:33:31
interesting that I can make some changes to the placement of the  the inception xform effect within the Composer update function. 


2017-04-06 01:35:46
I've moved the inceptionxform effect to the is_compositing enabled path way. Moving that block of functionality makes the transformation happen at different "pahases" of the update. I.m not entirely clear why. Just an intuition. Its looking very interesting placed where it is.  more fluid



2017-04-06 16:34:05
setting up at the  Hammer Theater in San Jose


2017-05-07 17:57:03
I gained some insights at LASTFEST2017, it was the most nuanced and interactive show thus far. There was a big payoff for staging it with dedicated gear, as I did. One unexpected consequences of that is that I now have a storage space - needed somewhere to stor ethe gear for easy deployment
.

I'm back to the project after some time away. Will organize my goals and thoughts a bit later but here are the outcomes I achieved

- invitation to speak at Piero Scaruffi LAZER talk in July
- private show being planned here with primary goal being promotion and a night of hallucinations that I want to turn into a portrait series.

- next steps?
- many more possibilities than I'd realized, maybe a bit afraid to say it out loud?

2017-05-07 18:02:11
stepping back into python and studying multiprocessing again.

2017-05-16 20:39:15
Feeling so blocked by upcoming talk and the private show I've been thinking about
How to stop feeling blocked? Do something now.
- work on my talking points
- collate current work
- update deepdreamvisionquest.com
- contact Piero S to discuss upcoming event and my topic
- create guest list for event
- transfer equipment from storage

2017-05-16 20:53:15
I've setup a local repository on the MacBook

2017-05-26 14:01:41
The upcoming LASER talk has been sublimating even as it seemed like procrastination.
The title:
	So Much Neural
The subject:
	I want to talk about how my life as a videogame designer has influenced my new work and describe the ways I learned to use 	psychedelic machine learning to look for Universal Images

The Theme:
	Deep Dreams, Universal Images

Notes
This talk answers the question, “where do the images come from”, “why these images are important”, “where do these feelings come from”,”I can’t take my eyes off it. Why?”, What is the meaning?

For show and tell,
- it uses a series of computed portraits with imagery produced by my Deep Dream Vision Quest neural video installation.
- full setup with magic mirror
- projected setup

What have I discovered from live shows
- people matter
- staging and setting matter
Where does the data come from and who owns it?
What do I get out of it?
Applications
- entertainment
- therapy
- outreach
- surveillance
- roleplaying

Talking Points

We live in a hyper modern world where things blur together, the categories are blending together. 

What does human mean now? The Othering. To be Other.


My mom is seeing AI in her camera. Its a filter that restyles the world like a painting. How is that app on her phone different than my work?

The Mandela Effect - why?

We seek to surface that which lies submerged – desire, guilt, fear, ambition – to bring to light the truth the waking mind keeps hidden
Why?
To find the Familiar in the Alien
Why?
Because the contrast is exciting
Why
Because there are Universal Images
Why
They resemble the classifications of a neural network
Why
The underlying behavior of learning machines must be universal
Why
Because the algebra and the architecture is the same

Therefore:
All perception begins as hallucination
Mental images from activated neural patterns  project outward as iterations in a feedback loop of recognition-reclassification
Neural patterns?
Yes. Archetypes. Geometric memories.  Arrays of filters.
Projected from where?
The Center
What is at the center?
Me. I am hiding something

<<<<<<< HEAD
2017-05-07 18:39:36
 The multiprocessing module allows you to spawn processes in much that same manner than you can spawn threads with the threading module.

2017-05-09 16:00:42
CTRL-J joins the line below to the end of the current line
CTRL-L selects the current line
CTRL-C copies current line if no selection
CTRL K,B toggle sidebarx


2017-05-09 17:01:15
Try and Except.
If an error is encountered a Try block execution is stopped and transferred down to the Except block. In addition to using an Except block after the Try block, you can also use the Finally block. The code in the Finally block will be executed regardless of whether an exception occurs.


2017-05-09 18:09:59
the join() method tells Python to wait for the process to terminate.
=======
What are some of the themes common to this imagery
Repetition
Embellishment
Replacement
Structure
Autocompletion
Suggestion
Shorthand
Radial Symmetry
Scale

2017-05-28 10:31:40
Configured Windows w Sourcesafe and so forth

2017-05-28 21:32:58
building the feature block on the main deepdreamvisionquest page
- create blog posts
    + Beginning
        * setup
        * testing
    + Middle
        * moments
        * best of
    + End (these are placed in a seperate media gallery accessible from top menu)
        * encounters (video)
        * portraits

2017-05-29 16:21:58
Not sure how much I really accomplished in this worksession. The site looks different. probably better. Definitely cleaner. But where is the new content?

2017-05-31 15:21:17
Reading up on the LASER talks


The LASERs are a national program of evening gatherings that bring artists and scientists together for informal presentations and conversation with an audience


Fromm Hall
2497 Golden Gate Ave
San Francisco, CA 94118

Fromm Hall hosts art studios, student housing, the Fromm Institute for Lifelong Learning, and Saint Ignatius parish offices.

Informal
35 minutes
assumptions: projector screen (how big)
USF, Fromm Hall, Berman Room, FR115

2017-05-31 16:13:19
The question I'm trying to answer is how can I show realtime hallucinations in the room?
Can I rely on the projector?
Should I consider my own projector?
Should I consider the full Deep Dream rig?

setup time needs to be minimal. talk is only 35m
need to setup and test before the talk

The talk is a show & tell
The showing is more epic when it points at an audience
With the right rig - could demonstrate specific effects & setups - camera, light

2017-05-31 16:23:42
requested more info about the space from @usfca

2017-06-01 08:46:15
no response from @usfca

2017-06-01 08:46:30
collating prior LASER abstracts


Mainland China has staged one of the most impressive economic booms in the history of the world, without a single recession in 30 years.The nation is now undergoing another transformation, from a manufacturing-based economy to an IT-based economy.The Chinese like to talk nonstop about "innovation", but "innovation" can have wildly different meanings in the USA and in China.

    THEME
    How does innovation transform global economies differently?

    OBSERVATION
    Innovation can have wildly different meanings in the USA and China

    WHAT PROMPTED OBSERVATION?
    The Chinese like to talk nonstop about innovation

    TOPIC
    Mainland China has staged one of the most impressive economic booms in the history of the world

    TOPIC MOVES FROM A TO B
    The nation is now undergoing another transformation from a manufacturing based economy to an IT based economy


The story of the development of the arts in Silicon Valley has just begun to be told.Its art history is filled with people who were often marginalized, people who stood up to the status quo, people with the guts and love to persevere and build a community that nourished all, at a time when that was not easy to do.It's time to tell the story.How did we get from the largely monochromatic, exclusive, and repressive landscape of the 1970s to where we are now? Silicon Valley blossomed in the last quarter of the 20th century with the formation of arts offshoots, spin-offs, and startups that tapped into the area's increasing ferment of ideas and involved myriad supporters across all walks of life.

    THEME
    It's time to tell the story about the art community in Silicon Valley

    OBSERVATION
    The area's increasing ferment of ideas involved myriad supporters across all walks of life.

    WHAT PROMPTED OBSERVATION?
    Silicon Valley art history is filled with people who were often marginalized

    TOPIC
    Silicon Valley blossomed in the last quarter of the 20th century with the formation of arts offshoots, spin-offs, and startups

    TOPIC MOVES FROM A TO B
    How did we get from the largely monochromatic, exclusive, and repressive landscape of the 1970s to where we are now?


Pantea Karimi presents and discusses her medieval and early modern scientific manuscripts research project. Karimi's research topics include: Medieval Math, Medieval Paper Wheel Charts Calculators, Medieval Cartography, Medieval Medicinal Botany and Optics. Through her work she invites the viewer to observe science and its history through the process of image-making. In her talk she presents the scientific manuscripts pages, the process of research and how she uses the visual elements in early science to create her art.

    THEME
    A decolonialized view of science history through the process of image-making

    OBSERVATION
    n/a

    WHAT PROMPTED OBSERVATION?
    n/a

    TOPIC
    The artist's medieval and early modern scientific manuscripts research project

    TOPIC MOVES FROM A TO B
    How she uses the visual elements of early science to create her art.



As an astronomer, I view new telescopes as a steadily increasing number of senses, new interfaces to the world, that bring otherwise inaccessible phenomena into my intimate awareness. I will present a brief history of the universe informed by this perspective. Most people on this planet have never met a scientists nor used a scientific instrument. I believe that part of the cultural change needed to build a sustainable society involves making scientific knowledge acquired through instruments an intimate part of daily life. Just as the inability of large banks were to respond to the daily needs of individuals led to the micro credit movement, I argue that scientific institutions are unable to respond to the scientific needs of individuals, and that a micro-science movement is needed. I will give examples of the work of artists that in my view are exemplars of intimate science

    THEME
    Making science intimate

    OBSERVATION
    Most people on this planet have never met a scientist nor used a scientific instrument

    WHAT PROMPTED OBSERVATION?
    As an astronomer, I view new telescopes as a steadily increasing number of senses, new interfaces to the world, that bring otherwise inaccessible phenomena into my intimate awareness.

    TOPIC
    The cultural change needed to build a sustainable society involves making scientific knowledge acquired through instruments an intimate part of daily life.

    TOPIC MOVES FROM A TO B
    Just as the inability of large banks to respond to the daily needs of individuals led to the micro credit movement, I argue that scientific institutions are unable to respond to the scientific needs of individuals, and that a micro-science movement is needed


New computer methods have been used to shed light on a number of recent controversies in the study of art.For example, computer fractal analysis has been used in authentication studies of paintings attributed to Jackson Pollock recently discovered by Alex Matter. Computer wavelet analysis has been used for attribution of the contributors in Perugino's Holy Family. An international group of computer and image scientists is studying the brushstrokes in paintings by van Gogh for detecting forgeries. Sophisticated computer analysis of perspective, shading, color and form has shed light on David Hockney's bold claim that as early as 1420, Renaissance artists employed optical devices such as concave mirrors to project images onto their canvases. How do these computer methods work? What can computers reveal about images that even the best-trained connoisseurs, art historians and artist cannot? How much more powerful and revealing will these methods become? In short, how is computer image analysis changing our understanding of art? This profusely illustrate lecture for non-scientists will include works by Jackson Pollock, Vincent van Gogh, Jan van Eyck, Hans Memling, Lorenzo Lotto, and others. You may never see paintings the same way again

    THEME
    How is computer image analysis changing our understanding of art?

    OBSERVATION
    You may never see paintings the same way again

    WHAT PROMPTED OBSERVATION?
    Sophisticated computer analysis of perspective, shading, color and form is increasingly used for attribution and authentication of artwork

    TOPIC
    New computer methods have been used to shed light on a number of recent controversies in the study of art.

    TOPIC MOVES FROM A TO B
    What can computers reveal about images that even the best-trained connoisseurs, art historians and artist cannot?


A very brief history of the accidental discovery of natural radio in the late-19th Century, the musical aesthetics of scientific research in the 1920s and 30s, and the beginnings of amateurism and arts in the second-half of in the 20th Century.

    THEME
    The electromagnetic Imaginary

    OBSERVATION
    n/a

    WHAT PROMPTED OBSERVATION?
    n/a

    TOPIC
    A very brief history of the accidental discovery of natural radio in the late-19th Century, the musical aesthetics of scientific research in the 1920s and 30s, and the beginnings of amateurism and arts in the second-half of in the 20th Century.

    TOPIC MOVES FROM A TO B
    Accidental discoveries and correlations

The "Sounds of Space" project is being developed to explore the connections between solar science and sound, to compare visual and aural representations of space data, mostly from NASA's STEREO mission, and to promote a better understanding of the Sun through stimulating interactive software. I will be talking about the work I am doing with musicians to sonify current solar wind data (particle data and magnetic fields) and images of the Sun.

    THEME
    Promote a better understanding of the Sun with interactive software

    OBSERVATION
    Comparing visual and aural representations of space data engages the public

    WHAT PROMPTED OBSERVATION?
    n/a

    TOPIC
    The "Sounds of Space" project is being developed to explore the connections between solar science and sound

    TOPIC MOVES FROM A TO B
    I will be talking about the work I am doing with musicians to sonify current solar wind data and images of the Sun.



Mat-forming Cyanobacteria in San Francisco Bay salt marsh ponds move in a gentle coordinate dance of 3.5-billion years, creating our oxygen atmosphere. I wanted to capture, in motion and music, a sense of this deep time and relentless movement.

    THEME
    Motion and Music 

    OBSERVATION
    Mat-forming Cyanobacteria in San Francisco Bay salt marsh ponds move in a gentle coordinate dance of 3.5-billion years creating our oxygen atmosphere

    WHAT PROMPTED OBSERVATION?
    Our oxygen atmosphere. 

    TOPIC
    Deep Time

    TOPIC MOVES FROM A TO B
    I wanted to capture, in motion and music, a sense of this deep time and relentless movement.

3D printed architecture has the ability to transcend the way that buildings are made today. 3D printers allow architects to be material morphologists.They expand our ability to construct because they open the door for us to test material, form and structure simultaneously and instantly. 3D printing is a sustainable method of manufacture and can take advantage of local and ecological material resources. In an era of throw away consumerism and over consumption, excessive energy use, too much waste, and toxic materials, architects have a responsibility to the public, and the planet, to change our mindset about what our buildings are made of, how they function, and to inform the manufacturing processes used to construct architecture. Our research challenges the status quo of rapid prototyping materials by introducing new possibilities for digital materiality.In this scenario it is not solely the computational aspects that have potential for material transformation but also the design of the material itself. Because of the nature of these materials, they can be sourced locally (salt, ceramic, sand), come from recycled sources (paper, rubber), and are by products of industrial manufacturing (wood, coffee flour, grape skins); this would situate them within the realm of "natural building materials". However, the expansive and nascent potential of these traditional materials, when coupled with additive manufacturing, offers unnatural possibilities such as the ability to be formed with no formwork, to have translucency where there was none before, extremely high structural capabilities and the potential for water absorption and storage, the materials that we all know as natural building materials are now unnatural building materials.

    THEME
    New possibilities for digital materials

    OBSERVATION
    The materials that we all know as natural building materials are now unnatural building materials.

    WHAT PROMPTED OBSERVATION?
    Traditional materials, when coupled with additive manufacturing, offer unusual possibilities

    TOPIC
    3D printed architecture has the ability to transcend the way that buildings are made today.

    TOPIC MOVES FROM A TO B
    Architects have a responsibility to the public, and the planet, to change our mindset about what our buildings are made of, how they function



Take Me To Your Dream (Dream Vortex) is a work-in-progress, a virtual installation for the KeckCAVES 3-D imaging facility at the University of California, Davis, and an artistic experiment with many layers of collaboration. In addition to the primary relationship with my scientific collaborator, geobiologist Dawn Sumner, there is a network of potential contributors including every researcher who works in the facility. This talk uses the experiences and challenges of the project as a way of thinking about collaborative processes in general,and as a way of finding creative gates in the fences between public/private, objective/subjective, traditional media/new media, and scientific/artistic forms of investigation.

    THEME
    How to collaborate with scientists

    OBSERVATION
    Take Me To Your Dream (Dream Vortex) is an artistic experiment with many layers of collaboration.

    WHAT PROMPTED OBSERVATION?
    In addition to the primary relationship with my scientific collaborator, geobiologist Dawn Sumner, there is a network of potential contributors including every researcher who works in the facility.

    TOPIC
    This talk uses the experiences and challenges of the project as a way of thinking about collaborative processes in general

    TOPIC MOVES FROM A TO B
    Finding creative gates in the fences between public/private, objective/subjective, traditional media/new media, and scientific/artistic forms of investigation.


A funny thing happened on the way to the millenium: The world went digital. Prophets had predicted for years that a single new digital medium would replace all the old analog media. What had been ink and paper, photographs, movies, and TV, would become just bits. Well, the Great Digital Convergence happened. It crept upon us unannounced, but it's here. This talk heralds that signal moment, a massive change in our culture. The elementary particle of the revolution is the much misunderstood pixel. The talk tackles head-on the fundamental mystery of digital-that spiky represents smooth, that the discrete stands for the continuous. How can that be? The full message is an explanation of how the whole digital world works and why it deserves our trust. The beginnings go back two centuries to a man who was almost beheaded and knew Napoleon too well. And to early last century when a Russian scientist, unknown to most Americans, defined the pixel while managing to stay out of the Gulag under the protection of a brilliant woman married to one of Stalin's bloodiest henchmen.

    THEME
    The talk tackles head-on the fundamental mystery of digital

    OBSERVATION
    Prophets had predicted for years that a single new digital medium would replace all the old analog media.

    WHAT PROMPTED OBSERVATION?
    It crept upon us unannounced, but it's here.

    TOPIC
    The full message is an explanation of how the whole digital world works and why it deserves our trust.

    TOPIC MOVES FROM A TO B
    The beginnings go back two centuries to a man who was almost beheaded and knew Napoleon too well. And to early last century when a Russian scientist, unknown to most Americans, defined the pixel while managing to stay out of the Gulag under the protection of a brilliant woman married to one of Stalin's bloodiest henchmen.


Black hole and cosmological horizons play a crucial role in physics.They are central to our understanding of the origin of structure in the universe, while continuing to provide vexing theoretical puzzles. They have become accessible observationally to a remarkable degree, albeit indirectly. I will review how horizons appear in general relativity and quantum field theory. Then I will move to a systematic study of their breakdown and its relevance -- or more precisely, `dangerous irrelevance' -- to thought experiments and real observations in specific situations. After describing the sensitivity of primordial cosmological perturbations to heavy degrees of freedom and large field values, I will share some results exhibiting the breakdown of effective quantum field theory for string-theoretic probes of black hole horizons.

    THEME
    Thought experiments compared to observations of black holes

    OBSERVATION
    Black hole and cosmological horizons play a crucial role in physics.

    WHAT PROMPTED OBSERVATION?
    They are central to our understanding of the origin of structure in the universe, while continuing to provide vexing theoretical puzzles. They have become accessible observationally to a remarkable degree, albeit indirectly

    TOPIC
    I will review how horizons appear in general relativity and quantum field theory.

    TOPIC MOVES FROM A TO B
    I will move to a systematic study of their relevance to thought experiments and real observations in specific situations.

2017-06-01 17:20:13
finished analysis of the provided abstracts, now I'm ready to write my own. Its going to clear up my own thinking too I expect.


2017-06-01 19:08:44
still thinking



Gary Boodhoo combines video games with machine learning to create interactive science fiction. He invents artificial experiences.

Deep Dream Vision Quest is a video synthesizer that creates multiplayer hallucinations. Live cameras reveal the world to a neural network which progressively misunderstands what it sees. Choosing between the front facing or back facing camera turns the AI dream into a mirror or a window.


note to self before I forget. Anyone who's ever wanted to "learn to code" needs to experience this moment to truly get it. The stakes seem so high to me right now, and looking back, I've put so much of myslef into understanding this idea and how to realize it. Learning python has been a big part of that. I didn't realize how beautiful the language is. Truly, its like Elvish. But right now - thinking through the trial and error of passing functions and parameters as part of a "program" that drives my artwork is the most challenging computer science ever. Its bitter to know that you could have done it differently, that you didnt understand something the way you thought, or that  you are almost certainly missing out on a basic concept, knowledge of which would make the current impasse invisible. Still - I'm hacking my waty to the solution, and its happening right now!

Experience an interactive psychedelic journey within a computer interface. Using the DeepDream convolutional neural network algorithm and real-time video feedback, the system turns your image into a vision of its own thought processes--a magic mirror. Questions about DeepDream, the magic mirror setup, and the spirit realm inside the machine are all welcome. Attendees will leave with an understanding of how neural networks may be used for image synthesis

Attendees will leave with an understanding of how neural networks may be used for image synthesis, and specific steps for creating their own Deep Dreaming Magic Mirror.

When I saw "Find Your Spirit Animal In A Deep Dream Vision Quest" - I quietly hoped I would meet someone that I could talk to. I sometimes yearn for belonging, but I refuse to shapeshift just to fit into someone else's tribe.

We found them by showing the world to a neural network through a live camera

Our interactive video installation shows the world to a neural network through a live camera. Clusters of artificial neurons light up when the network recognizes features it has learned before. Using Google's Inceptionism method, we synthesize imagery (dreams) from neural signals. We loop these graphics and project them back into the installation space.

But, until the camera detects movement in the space, the computer dreams about the last thing it saw. The audience and the environment dissolve. Strange creatures emerge from a familiar landscape. Only in stillness are they visible to us, only in motion are we visible to them.

I've presented living machine hallucinations to audiences for the past year as a way to share my own reactions to creative AI. It is still unclear where the intelligence emerges and where it ends. The best moments are when the environment itself seems to have an agenda. It wants to turn you into a kind of reptile. It wants to find ghosts(!) That's science fiction theatre, but is it a mirror or a window? 

This talk answers the question, “where do the images come from”, “why these images are important”, “where do these feelings come from”,”I can’t take my eyes off it. Why?”, What is the meaning?

For show and tell,
- it uses a series of computed portraits with imagery produced by my Deep Dream Vision Quest neural video installation.
- full setup with magic mirror
- projected setup

What have I discovered from live shows
- people matter
- staging and setting matter
Where does the data come from and who owns it?
What do I get out of it?
Applications
- entertainment
- therapy
- outreach
- surveillance
- roleplaying

Talking Points

We live in a hyper modern world where things blur together, the categories are blending together. 

What does human mean now? The Othering. To be Other.


One of my parent's friends asked me about the AI in his camera. The one that makes the video look like a painting. How is that app different than my work?



Why I've presented living machine hallucinations to audiences for the past year. 
    - I seek to surface the stories that lies submerged underneath vision
Why?
    - To better understand the images I respond to and prepare for consumption
Why?
    - To recognize the alien as familiar, and to recognize how alien the familiar is

Why
Because there are Universal Images
Why
They resemble the classifications of a neural network
Why
The underlying behavior of learning machines must be universal
Why
Because the algebra and the architecture is the same

Therefore:
All perception begins as hallucination
Mental images from activated neural patterns  project outward as iterations in a feedback loop of recognition-reclassification
Neural patterns?
Yes. Archetypes. Geometric memories.  Arrays of filters.
Projected from where?
The Center
What is at the center?
Me. I am hiding something

What are some of the themes common to this imagery
Repetition
Embellishment
Replacement
Structure
Autocompletion
Suggestion
Shorthand
Radial Symmetry
Scale

2017-06-01 21:54:59
lots to think about

THEME
Where do the images come from?



OBSERVATION


WHAT PROMPTED OBSERVATION?
One of my parent's friends asked me about the AI in his camera. The one that makes the video look like a painting. How is that app different than my work?

TOPIC
Why I've presented living machine hallucinations to audiences for the past year.

Well? Why did you do it?


TOPIC MOVES FROM A TO B


Well? Why did you do it?
Fame, glory, getting out of my comfort zone, curiosity

Why did you keep on doing it?
The code kept getting better and suggesting new directions. When people saw it, their reactions suggested new ways of coding and presenting. Their reactions included silence and pantomime. I saw an opportunity to shape these behaviors further with new code and stagecraft. I continue to search for ways to extend the moments of surprise and extend them into meaningful experiences. I've always maintained the fiction that this was some kind of videogame, until it became a truly reactive system. As I've shown it, I have observed that some people just "get it" more than others. The repeated but hallucinatory patterns that emerge in response to activity in front of the camera changes that activity. Currently I see this kind of feedback loop iterating (recursing) 2-3 times. Someone does something and sees it multiplied on screen, they pose and point at the screen and the image continues to change. They learn to shift their posture and play with the camera (which to my surprise) has turned out to be a hugely responsive game controller.

What does it do?
The video installation shows the world to a neural network machine through a live camera. The machine reconstructs what it sees. We project that image back into the installation space. Until the machine detects motion, it dreams about the last thing it has seen. With each uninterrupted dream cycle the transformation of this memory becomes more extreme. Strange creatures emerge from alien landscapes. Only in stillness are they visible. They fade away when you move. This reflective "hurry up and wait" quality provides the basis for emergent gameplay. 

Why did you make it?
A year later, It is still unclear where the intelligence emerges and where it ends. The best moments are when the environment itself seems to have an intention. It likes some things, and perhaps some people more than others. It wants to turn you into a kind of reptile. It wants to find ghosts(!) That's science fiction theatre, but why is it so easy, and is it a mirror or a window? 

2017-06-02 10:38:35
I've generated several schematics for potential talks. Here they are


#
    THEME
    Hacking the solution

    OBSERVATION
    Anyone who's ever wanted to "learn to code" needs to experience this moment to truly get it.

    WHAT PROMPTED OBSERVATION?
    The trial and inference of passing functions and parameters as part of a "program" that creates artwork is the most challenging computer science ever.

    TOPIC
    How I use neural network machines to make pictures

    TOPIC MOVES FROM A TO B
    I've presented living machine hallucinations to audiences for the past year as a way to share my own reactions to creative AI.

#
    THEME
    Where they come from

    OBSERVATION
    I seek to surface that which lies submerged

    WHAT PROMPTED OBSERVATION?
    One of my parent's friends asked me about the AI in his camera. The one that makes the video look like a painting. How is that app different than my work?

    TOPIC
    How I use neural network machines to make pictures

    What I've learned from presenting machine hallucinations to humans and living rooms for the past year. 

    TOPIC MOVES FROM A TO B
    I've presented living machine hallucinations to audiences for the past year and am discovering a design language to extend moments of surprise into meaningful experiences



make the theme more active:
Where they came from

// doing something. Finding
Find your spirit animal in a deep dream vision quest

Deep Dreams, memories and confessions

Conspiring to uncover a universal interface

Confessions of a universal interface

finding the universal interface to the memory palace

Finding the universal interface to legacy reality

Uncovering their tracks

Hunting for a universal interface

Uncovering rituals with widespread deep dreaming

Improving the quality of ritual interfaces for humans

Deep Dreams, high scores and epic dread

High sco


Deep Dreams, Omens and Premonitions.

Sharing memories with machine intelligence

Deep Dream, Ritual Interface
Deep Dream, Ritual Interface to the Library of Babel


Machine Learning teaches us something amazing. It doesn't take much to invent the world. Any technology capable of recognizing images must also create them. Wherever we find aliens they'll be artists too. 



2017-06-03 12:03:24
What's not being said:
My experiences over the years with an intense lucid dream where I asked Jesus to help me.
My experiences with psychedelics, specifically the reality that DMT uncovered.
Any mention of legacy reality


It's not that I seek to uncover the submerged. It's that the visual memories shared by machines and people conspire to uncover the truth of a universal interface. 

The surprising emergent property of hyperplatonic digital is archaic dreamtime. Everything, everywhere is an event horizon, infinitely receding and
The visual memories shared by people and machines conspire to reveal universal images. The kinds of images that build dreams and over time build civilizations. The design space is a metaphor that constructs legacy reality.
[example ]

Legacy Reality means the kind of reality that can be sensed with a camera. An electromagnetic field really. Functionally this is the source of the datasets a visual intelligence can learn to classify.

Hallucination means that the memories of Legacy Reality are reconstructed visually, in a feedback loop, running on any hardware capable of representing a large enough array of summed multiplication. Like a visual cortex, and also like a GPU.

2017-06-03 17:02:57
Wherever we find aliens they'll be artists too. 

can Alien be removed from this statement, while preserving the intent? Its too much of a shortcut. I don't like how its becoming a default word.

Wherever we find ourselves, we'll be artists
When we find ourselves we'll be artists
arists find selves wherever they are
The 


The eye as transmitter is found worldwide, as is a prohibition against staring at people.

Even in our society you don’t look directly at someone for any length of time without speaking. People in prison avoid eye contact since it’s seen as an aggressive act.

Young children believe that the eye is a transmitter and that the eye beams of people can mix or clash.

In the comics, Superman is able to heat a hotdog or open a safe with his eye beams.

The eye objectifies, which is why we speak of “sex objects”. Not enough attention has been given to the way in which cultures train people to use their senses. 

In medieval times the dictum was “fides ex auditu” (faith comes from hearing) but by the Renaissance the Protestants were reading the Bible. 

Another medieval dictum was “nil intellectu quod non prius in aliquodo modo in sensibus”. There is nothing in the mind which is not first, in some manner, in the senses.

2017-06-03 17:19:53
1st draft

    THEME
    The memories shared by machines and people conspire to uncover universal images. Where do they come from?


    OBSERVATION
    It doesn't take much to invent the world. Any system capable of recognizing images must also create them.


    WHAT PROMPTED OBSERVATION?
    As I coded variations on the feedback loop used to create pictures, I soon realized that people were completing the synthetic images with their own memories and expectations. Perception is a kind of hallucination made up from universal images which are mirrored by the learned classifications of a neural network.


    TOPIC
    The surprising emergent property of Big Data is the archaic dreamtime we remember from 50000 years ago.


    TOPIC MOVES FROM A TO B
    I've presented living machine hallucinations to audiences for the past year and in that time have discovered a design language to extend moments of surprise into long term meaningful experiences

what's missing?
no reference to cargo cult of machine intelligence. The imagined internal life of a machine intelligence is so much bigger than the machine intelligence. Is this just another way of expressing surprise that human beings seem much smarter than they need to be?

2017-06-03 18:30:44
does the topic involve the audience sufficiently?
what's so interesting about the archaic dreamtime then?
- we all share it at our most vulnerable
- animals share it too
- maybe it can be found outside of a nervous system

what's important to my mom about the archaic dreamtime?
- it draws a line between the unknown and the unknowable
- the wellspring of spirituality, and maybe even hope
- the spirit of the age (legacy reality) is shaped by archaic dreams. What dreams may come aren't random, but instead reactive

Unpack that - reactive?
Like a computer UI, the reactive spirit of the age isn't waiting for input, its always creating even when surrounded by darkness. Interfaces like this uplift the "user" into communion with the Unknowable Unknown. The Alien. The Other. The Electromagnetic Imaginary. The Mystery.


Psychedelic AI space erotica
Psychedelic AI space invasion
Psychedelic AI space exploration

The psychedelic AI cargo cult of machine intelligence

Deep Dream, a psychedelic creative intelligence
Deep Dream Vision Quest for a 

Psychedelic space invader

You know all those ancient aliens you hear about in the news? I'm the worst one.

Human encounters with a gregarious creative intelligence in quest of a universal interface

Quest for a universal interface

Quest for an automated dreamtime

deep dream vision quest for creative intelligence

Portraits of a gregarious creative intelligence

Machine Hallucination

Science Fiction Thriller

Cargo, Mana and Taboo

Deep Dream Cargo Cult

As such, commodity fetishism transforms the subjective, abstract aspects of economic value into objective, real things that people believe have intrinsic value.[1]

Millenarianism has been found through history among people who rally around often-apocalyptic religious prophecies that predict a return to power, the defeat of enemies, and/or the accumulation of wealth. These movements have been especially common among people living under colonialism or other forces that disrupt previous social arrangements.

A cargo cult is a millenarian movement first described in Melanesia which encompasses a range of practices and occurs in the wake of contact with more technologically advanced societies. The name derives from the belief which began among Melanesians in the late 19th and early 20th century that various ritualistic acts such as the building of an airplane runway will result in the appearance of material wealth, particularly highly desirable Western goods (i.e., "cargo"), via Western airplanes.



THEME
Memories shared by machines and people reveal universal images. Where do they come from?


OBSERVATION
It doesn't take much to invent the world. Any system capable of recognizing images must also create them.

The surprising emergent property of Big Data is an iteractive and archaic dreamtime.


WHAT PROMPTED OBSERVATION?
As I coded variations on the feedback loop used to create pictures, I soon realized that people were completing the synthetic images with their own memories and expectations. Perception is a kind of hallucination made up from universal images which are mirrored by the learned classifications of a neural network.


TOPIC
How I use neural networks to find pictures


TOPIC MOVES FROM A TO B
I've presented living machine hallucinations to audiences for the past year and in that time have discovered a design language to extend moments of surprise into long term meaningful experiences


THEME
Serendipity rewards stillness

OBSERVATION
AI in 2017 may be understood as a cargo cult (?) 
[not uninteresting - but does it leads the conversation away from or towards the role of serendipity ]

WHAT PROMPTED OBSERVATION


TOPIC
How I use neural networks to find pictures



THEME
Serendipity



Dreams emerge from a process called gradient descent. Neural activity is added back to the picture that caused it. Thus creating a feedback loop which serves to make any detected features more like themselves. The software doesn't generate fully realized images all at once. Instead the neural network dreams repeatedly, building up a picture from nothing but statistics. Its incredible.

Deep Dream is a lens that reveals how visual concepts are represented by a learning machine. The computer simulates a vast cortical array. This geometry is called a neural network. Neural, because it is said to behave like a nervous system. 


Neural networks come in different shapes and sizes. Deep Dream Vision Quest uses a popular implementation of Google's Inception architecture (like the movie) called GoogLeNet. It may come as a surprise, but the network doesn't contain images. It contains only habits, which are the learned weight values of neural connections. GoogLeNet was trained on over 1 TB of images, but is itself only 50 MB in size. 

A
This is a story of a guy who saw  on the internet and became curious about how they were made. He was a hacker and an artist and an on-again off-again Radical Platonist who wanted to put everything inside of a box

B
Decades of psionic research provided tantalizing hints. But what can you say about the Unspeakable? 

Yes, he had faced UFO's and the creatures that drive them. He had regarded the reptile mammal insect plant entity inside himself with Dread and Awe. Most of all he was stubborn.

C
Showing it to people

As he coded variations on the feedback loop used to create pictures, he realized that people were completing the synthetic images with their own memories and expectations. Perception is a kind of hallucination made up from universal images which are mirrored by the learned classifications of a neural network.

Then he saw a ghost. He pointed the camera at the empty auditorium and turned around to finish setting up the equipment. Meanwhile on the television, something emerged from the vacant seats. Spirit animals, machine elves. The same hybrids

The machine dreams were alien but also familiar. The pictures it made apparently lack any logic beyond the amplified coincidences found in the source material.

identify your unique spin on a universal theme
I am an artist who uncovers the familar in the alien
I am the oldest son who welcomes the stranger
I lifted the covers and found a spider
The other one, in the mirror.

2017-06-10 22:03:24
I just want to talk about the work I'm currently doing and what has led me to this point. The unexpected insight I gained along the way was that this technology can transform environments and change the way people behave.


Bio:
Gary Boodhoo combines video games with machine learning to invent interactive science fiction. He arrived in the United States from Jamaica along with the first personal computers determined to find or build a new world.
Millions of players around the world use the game interfaces he directed and designed for Madden NFL, The Sims, Star Wars: The Force Unleashed and The Elder Scrolls Online. My design studio skinjester, inc. helps creative organizations build humane software. 

Title:
Deep Dreams, Omens and Premonitions
Human encounters with a gregarious machine intelligence

How is live machine hallucination different than the app on my phone

2017-06-11 13:16:52
You've not yet asked what the audience wants. I know my own motivations for wanting to present but why did that person sitting in front of me bother to come? How much can you find out about them?

WANT
Curiosity
The subject of machine learning fits into their view of the world
Desire to feel smart and share personal observations
They arrive with something they want to express about the subject although they may not have put it into words (its hard!) They came to be entertained. Show them how to get what they want. How do you know what they want?

They wanted to feel smart
They wanted to feel like their interest is validated
They want to learn - guide them through a step by step analysis of how 

No one comes to these talks without an interest in the subject.
It may be that some people are figuring it all out themselves and are putting the presentation on a spectrum of what they know or assume

The importance of credibility
My credibility validates their interest

They came because they have an interest and want to see where my story fits into their personal narrative.

Some people just came to meet other people. Maybe make some kind of personal connection. Maybe find perspective.

No one goes to these things to judge me, and my big fear is that I'll be judged. 

What parts of myself have I not shown?
- the arcane researcher pushing my understanding to understand how it works
- the person who spent money to make it work faster
- the self taught everyman who was born special, and this was why
What parts of myself has it felt best to share?
 - the arcane setup that kept evolving and led me to this moment, it was epic just making it work at all! Made me feel like a real hacker
I'm going to talk about something your parents and the clergy told you never to discuss in polite company.

If you don't think you're in sales, I want you to think about the last time you wanted sex...

In this fun and personal talk, Caroline shares a story of moving from stage-paralysis to expressive self. Accompanied by an unusual prop, she encourages us to use our voice as an instrument and really find the confidence within. 



As I child I wondered if I'd seen everything a person could see. I wasn't jaded yet, but maybe everything to come would be just a combination of all the patterns I was already familiar with. I wondered - could there be images that no one had imagined yet?


In this talk, Gary shares a story of how he befriended an intelligent machine and became an artist again.  Learning to code in Python was the gateway


 We train the neural network to recognize images and then "run it backward" by amplifying the signals it makes during image recognition and adding them back to the image it attempts to recognize. This leads to wild visual feedback which to us appears as a "machine hallucination". Yet how interesting it is that these hallucinatory images resonate with our own internalized visual language. The expression of which has resonated throughout human history in our cave art and our dreams. As soon as I connec

In traditional computing decisions are yes/no, true/false affairs. Neural computation is a bit different. Instead, decisions emerge from a little more of this, a little less of the other thing. Choices are more like habits. Learning then, is the process of adjusting all the biases so a neural network gets into the habit of recognizing new input. Machine learning is the art of getting it to do this on its own.



An alien intelligence surrounds us. Even now, in this very room.  

To achieve these results we've constructed artificial memories that represent more than just data, they are a model of nervous systems work. 

We call them neural networks. 

By doing so, we gain a better understanding of how our own minds work. Specifically, how do we understand what we see. 




Machine learning personifies how to extract intelligence from the environment, whatever that environment happens to be. The underlying assumptions of a learning machine are shaped by its training. Neural networks have habits, and with the right training they can get into the habit of recognizing spam email as or .

Image classification and the deep Dream algorithm are both deterministic. Given the same image, the machine will draw the same hallucination every time. But the world is less deterministic than the model. Showing the outside world to the network with a live camera, the input is never the same.

2017-07-11 00:26:43
getting hung up on the background section
- deep dream
- style transfer








The software doesn't generate fully realized images all at once. Instead the neural network dreams repeatedly, building up a picture from nothing but statistics.

2017-06-13 13:26:54
LASER Talk Summary:

HUMAN ENCOUNTERS WITH A GREGARIOUS LEARNING MACHINE

Suddenly, computers are good at seeing and understanding. Learning machines have arrived, bearing unexpected cargo. The surprising truth behind artificial intelligence is that Mind emerges from the environment. 

In 2015 a team at Google led by Alexander Mordvintsev released the first "Deep Dream" images to an amazed internet. These were instantly recognizable as photographs of the psychedelic experience. The algorithm is a dozen lines of code. It exaggerates a provided picture using habits the machine has learned.  It's a deterministic process. For any given image, the machine constructs the same hallucination every time.

I create video installations that show the world to a learning machine through a live camera. Deep Dream Vision Quest is a neural image synthesizer that creates multiplayer hallucinations. Although the algorithm is predictable, the world is not. At live performances I'm often asked where the images come from. I've come to recognize how easy it is for humans to complete them with our memories. In this talk I describe how I use stagecraft, creative coding, and game design to make pictures of Minds.


2017-06-13 14:16:21
TITLE:
Human encounters with a gregarious machine intelligence

[identify your unique spin on a universal theme]
THEME
universal: what is the nature of perception?
A mirror is a mask that looks at you

OBSERVATION
Intelligence emergences from the environment

PROMPT
The same program that identifies spam in your inbox can also identify a pedestrian in your car. Machine learning is the study of how to generalize information efficiently. Big Data 

TOPIC
How I use neural networks to find pictures

TOPIC MOVES FROM A TO B
I've presented living machine hallucinations to audiences for the past year and in that time have discovered a design language to extend moments of surprise into long term meaningful experiences


This time, with proofreading. Thanks Piero. G

LASER Talk, 11 July 2017


Human Encounters With a Gregarious Learning Machine

Suddenly, computers are good at seeing and understanding. Learning machines have arrived, bearing unexpected cargo. The surprising truth behind artificial intelligence is that Mind emerges from the environment. 

In 2015 a team at Google led by Alexander Mordvintsev released the first "Deep Dream" images to an amazed internet. These were instantly recognizable as photographs of the psychedelic experience. The algorithm is a dozen lines of code. It exaggerates a provided picture using habits the machine has learned.  It's a deterministic process. For any given image, the machine constructs the same hallucination every time.

I create video installations that show the world to a learning machine through a live camera. Deep Dream Vision Quest is a neural image synthesizer that creates multiplayer hallucinations. Although the algorithm is predictable, the world is not. At live performances I'm often asked where the images come from. I've come to recognize how easy it is for humans to complete them with our memories. In this talk I describe how I use stagecraft, creative coding, and game design to make pictures of Minds.

2017-06-25 16:55:26
Bringing Deepdreamvisionquest.com site into the modern era again. Working out details of the upcoming LASER talk

2017-06-25 17:43:45
Questions:P

Where does the idea that neurons are the basis of the Mind come from? Is it true?

Expressive mode, regenerative mode

2017-06-25 18:04:20
Shifting focus back to immediate needs of the website. What's missing here?
Wht prevents me from sharing this w peers, colleagues, new contacts> Obviously insecure about missing something

2017-07-08 17:03:27
working on the presentation now.
computer at the facilities is a macintosh with keynote and powerpoint installed
- test inclusion of local video content in a powerpoint doc
- do this work on the mac


2017-07-08 17:57:33
Shifted to MacOS and looking thru keynote
Installing Powerpoint here as well


2017-07-08 18:15:46
Artists frequently focus only on their own work as if it happened in a vacuum, while the audience really likes to place it in a context; sacrificing 10 minutes of the 20 for a survey of the field is worth it: they will appreciate the following 10 minutes a lot more. One of the rare standing ovations at a LASER talk was given to Robert Buelteman, who managed to tell the story of photography from the beginning to his own work in 20 minutes. I bet all the people who heard that talk still remember it to this day.


2017-07-08 18:42:32
Human Encounters With a Gregarious Learning Machine




2017-07-09 15:51:24
after touching it for a while yesterday, I've determined the structure of the presentation

Presentation structure

Start at the end first with a montage

These are my outcomes 
- Art 1
    - Style transfer series
- Art 2
    - Pre-rendered 
- Art 3
    - Live [postprocess]
- Art 4
    - Live [encounter loop]

How it began
- What is a neural network?
- They only see what they have learned to see and we feel the same. 
- Show misidentification 
- Misidentification in nature
- world of faces 
- Show hallucination of imagenet class
- What is deep dream?
    - Show example
- What is style transfer?
    - Show example


Something is missing
Live Camera
- People
    - Too much emphasis on the learning machine.
    - Not enough emphasis on how people react to the machine 
- The Environment
    - Live camera
    - Infinite diversity of the real world no matter how mundane 

I found the missing thing

Multiplayer hallucinations
- Social encounters 
- The environment contributes far more than the technology
- Stagecraft
    - Crafting how the experience is presented in social spaces
    - Mounting a 50” TV vertically did 2 things
        - Participants stand close to it like a magic mirror
        - Participants slow down
        - The generative images read more like a painting than a TV

What happens next?
- Its not an app, its an encounter
- Broaden audience 
    - Storefront installations
    - Trade Shows
    - Hotels
- Interdisciplinary collaboration
    - Dancers
    - Actors
    - Musicians
- Projection on architecture
- Smart cameras
    - Drones
    - Depth sensing
- End with a call to action


2017-07-10 10:45:05
- slides: deep dream description
- slides: style transfer description


2017-07-11 03:44:21
Comnpleted 1st draft presentation


2017-07-11 11:38:46
collecting talking points


2017-07-11 14:43:50
rehearsing


2017-07-11 15:50:16
getting better

University of San Francisco 
2130 Fulton Street 
SF, CA 94117 
Fromm Hall - Berman Room 
2130 Fulton Street, San Francisco, CA 94117-1080 


Ville-Matias Heikkilä
www.youtube.com/watch?v=UFVB5rnqjyY


2017-07-12 08:11:29
Presentation last night was a success.


2017-07-12 09:08:04
LASER Talk Presentation Notes
also add these to squarespace as notes

Presentation structure

Start at the end first with a montage

These are my outcomes 
- Art 1
    - Style transfer series
- Art 2
    - Pre-rendered 
- Art 3
    - Live [postprocess]
- Art 4
    - Live [encounter loop]

How it began
- What is a neural network.
- Training and Classification
- Misidentification (and interpretation)
- Deep Dream
- Style Transfer


- They only see what they have learned to see
- Training and classification
- ImageNet
- Show misidentification 
- Misidentification in nature
- world of faces 
- Show hallucination of imagenet class

- What is deep dream?
    - Show example. What about this example interests me?
- What is style transfer?
    - Show examples. What about this example interests me?


Something is missing
Live Camera
- People
    - Too much emphasis on the learning machine.
    - Not enough emphasis on how people react to the machine 
- The Environment
    - Live camera
    - Infinite diversity of the real world no matter how mundane 

I found the missing thing

Multiplayer hallucinations
- Social encounters 
- The environment contributes far more than the technology
- Stagecraft
    - Crafting how the experience is presented in social spaces
    - Mounting a 50” TV vertically did 2 things
        - Participants stand close to it like a magic mirror
        - Participants slow down
        - The generative images read more like a painting than a TV

What happens next?
- Its not an app, its an encounter
- Broaden audience 
    - Storefront installations
    - Trade Shows
    - Hotels
- Interdisciplinary collaboration
    - Dancers
    - Actors
    - Musicians
- Projection on architecture
- Smart cameras
    - Drones
    - Depth sensing
- End with a call to action

——
Dictionary
ILSVRC12 
Is a subset of the ImageNet database used for a popular machine learning challenge in 2012. Sometimes just referred to as ImageNet - as in “trained on ImageNet”

Some Facts
Neural Networks have been successfully applied to a wide range of data-intensive applications
Source: http://www.alyuda.com/products/forecaster/neural-network-applications.htm

Finance
Stock Market Prediction
Credit Worthiness
Credit Rating
Bankruptcy Prediction
Property Appraisal
Fraud Detection
Price Forecasts
Economic Indicator Forecasts

Medicine
Medical Diagnosis
Detection and Evaluation of Medical Phenomena
Patient's Length of Stay Forecasts
Treatment Cost Estimation

Operations
Process Control
Quality Control
Retail Inventories Optimization
Scheduling Optimization
Managerial Decision Making
Cash Flow Forecasting
Scheduling

Science
Pattern Recognition
Recipes and Chemical Formulation Optimization
Chemical Compound Identification
Physical System Modeling
Ecosystem Evaluation
Polymer Identification
Recognizing Genes
Botanical Classification
Signal Processing: Neural Filtering
Biological Systems Analysis
Ground Level Ozone Prognosis
Odor Analysis and Identification

Education
College Application Screening
Predict Student Performance

Data Mining
Prediction
Classification
Change and Deviation Detection 
Knowledge Discovery
Response Modeling
Time Series Analysis

Sales
Sales Forecasting
Targeted Marketing
Service Usage Forecasting
Retail Margins Forecasting

Human Resources
Employee Selection and Hiring
Employee Retention
Staff Scheduling
Personnel Profiling

Energy
Electrical Load Forecasting
Energy Demand Forecasting
Short and Long-Term Load Estimation
Predicting Gas/Coal Index Prices
Power Control Systems
Hydro Dam Monitoring

Machine Vision
Animation
Art
Automated vehicles
Facial Recognition
Object and Scene Recognition
Photography
Robotics



2017-07-12 09:26:59
working on LAST Festival blog post


2017-07-12 10:00:38
CODAME slides for Matchbox Talk due 7/14, presentation is on 7/20 *next Thursday)

3 minute artist talk: Randy Reyes + Gary Boodhoo. After investigating each other for a week, we meet for the first time and present 10 "facts" in 3 minutes. Happy hour after.




2017-07-17 08:15:22
put together a map for talk about Randy.
Estimated 7hrs to completion of this project


2017-07-20 08:25:17
completed final edit for slides last night
- confirm w Jordan that he's seeing them
- notes
- rehearsal


2017-07-20 08:25:55
spending this am updating deepdreamvisionquest.com
>>>>>>> master





