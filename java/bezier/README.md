This is a test to see how to write a Processing sketch as a proper java app.
I think I kind of prefer it this way. 

Create a `libs` folder. Then download Processing 4 and copy its `core.jar`
into that folder. That's because Processing 4 doesn't seem to be available 
in any online repository yet.

Run the app using `./gradlew run`. For me, `gradle run` fails half the time 
and I can't figure out why. Anyway, you can specify the window size via 
the command line like this: `./gradlew run --args="800 600"`.
