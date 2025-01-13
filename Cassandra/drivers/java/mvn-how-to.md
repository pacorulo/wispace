# How to create and execute a jar file with maven

1. Create the mvn folder/project structure:

```
mvn archetype:generate -DgroupId=com.datastax.astra -DartifactId=jdriver -DpackageName=com.datastax.astra -Dversion=1.0-SNAPSHOT -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

2. Previous step will create a folder named jdriver (-DartifactId) and under it we need to create the *pom.xml* file:

```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.datastax.astra</groupId>
  <artifactId>jdriver</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>jdriver</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
```

3. The folder/file structure under our main directory will be:

```
src/main/java/com/datastax/astra/App.java folders and file
src/test/java/com/datastax/astra/App.java folders and file
```

4. Now, with 'mvn intall' you will just create, compile, test, package, and install the most straightforward maven project

5. So now, only execute the jar file:

```
$ java -cp target/jdriver-1.0-SNAPSHOT.jar com.datastax.astra.App
Hello World!
```

> _Source: https://www.codekru.com/maven/how-to-create-and-run-a-maven-project-using-command-line_
