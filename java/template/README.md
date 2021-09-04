This is a template for a processing sketch using Gradle and Java. You need Java 11.

Stuff you should rename:
- the main Java file in src/main/java/
- the main class
- the mainClass in build.gradle

Make a `libs` folder and put the Processing 4 `core.jar` inside it.

Run the app using `./gradlew run`. Specify the window size via the command line like this: `./gradlew run --args="800 600"`.
