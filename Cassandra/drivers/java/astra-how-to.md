## Connect to [Astra DB](https://astra.datastax.com/signup?utm_source=google&utm_medium=cpc&utm_campaign=ggl_s_emea_brand&utm_term=datastax%20astra&utm_content=brand-astra&gad_source=1&gclid=CjwKCAiA0rW6BhAcEiwAQH28IuGncWKUjENBEq5O_YOk2pMnWQQGoVv9feWAswdE46qmDPunQxD4XBoCzZYQAvD_BwE) by using Maven

1. Install java-jdk
  
    ```
    sudo apt install openjdk-11-jre-headless
    ```
    Check version: `java --version`

2. Install Maven

   2.1 Download mvn frpom [Mvn Apache](https://maven.apache.org/download.html)
   
   2.2 Unzip: `tar xzvf apache-maven-3.9.9-bin.tar.gz`
   
   2.3 Create folder: `mkdir /bin/mvn`

   2.4 Add path: `PATH=/bin/mvn/apache-maven-3.9.9/bin:$PATH`

   2.5 Check version: `mvn -v`

4. Download SCB from Astra

5. Generate a token
    ```
    {
      "clientId": "blablabla",
      "secret": "secret_blablablablablablabla",
      "token": "token_blabla"
    }
    ```
5. Create a `pom.xml` file at the top of your source java folder structure (it will be at the same level of the src folder that will be created on next step)

    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
      <modelVersion>4.0.0</modelVersion>
      <groupId>com.datastax.astra</groupId>
      <artifactId>jdriver</artifactId>
      <version>1.0</version>
      <!--packaging>jar</packaging>
      <version>1.0</version>
      <name>jdriver</name>
      <url>http://maven.apache.org</url-->
      <dependencies>
        <dependency>
          <groupId>com.datastax.oss</groupId>
          <artifactId>java-driver-core</artifactId>
          <version>4.13.0</version>
        </dependency>
      </dependencies>
    </project>
    ```

    Some more tags at groupID level (at the beginning and commented out above)

6. Create java folder structure

    ```
    mkdir -p src/java/main
    ```

7. Create the java file under previous folder 
    ```
    /*
     * Copyright DataStax, Inc.
     *
     * Licensed under the Apache License, Version 2.0 (the "License");
     * you may not use this file except in compliance with the License.
     * You may obtain a copy of the License at
     *
     * http://www.apache.org/licenses/LICENSE-2.0
     *
     * Unless required by applicable law or agreed to in writing, software
     * distributed under the License is distributed on an "AS IS" BASIS,
     * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     * See the License for the specific language governing permissions and
     * limitations under the License.
     */
    //package com.datastax.astra;
    
    import com.datastax.oss.driver.api.core.CqlSession;
    import com.datastax.oss.driver.api.core.cql.ResultSet;
    import com.datastax.oss.driver.api.core.cql.Row;
    import java.nio.file.Paths;
    
    public class jdriver {
    
      public static void main(String[] args) {
    
        // The Session is what you use to execute queries. It is thread-safe and should be
        // reused.
        //try (CqlSession session = CqlSession.builder().build()) {
        try (CqlSession session = CqlSession.builder()
          .withCloudSecureConnectBundle(Paths.get("/home/vagrant/scb/secure-connect-java.zip"))
          .withAuthCredentials("${clientid}","${token}")
          .build()) {
          // We use execute to send a query to Cassandra. This returns a ResultSet, which
          // is essentially a collection of Row objects.
          ResultSet rs = session.execute("select release_version from system.local");
          //  Extract the first row (which is the only one in this case).
          Row row = rs.one();
    
          // Extract the value of the first (and only) column from the row.
          assert row != null;
          String releaseVersion = row.getString("release_version");
          System.out.printf("#########################################################################################################");
          System.out.printf("#########################################################################################################");
          System.out.printf("#########################################################################################################");
          System.out.printf("#########################################################################################################");
          System.out.printf("#########################################################################################################");
          System.out.printf("Cassandra version is: %s%n", releaseVersion);
          System.out.printf("#########################################################################################################");
          System.out.printf("#########################################################################################################");
          System.out.printf("#########################################################################################################");
          System.out.printf("#########################################################################################################");
          System.out.printf("#########################################################################################################");
        }
      }
    }
    ```

8. Package it with maven (at the src level, together with the _pom.xml_ file) with the below command (it will clean any previous package, but also 'verify' and 'package' the project)

    ```
    mvn package 
    ```

    You will get an output like:

    ```
    [INFO] Building jar: /home/vagrant/java/target/jdriver-1.0-SNAPSHOT.jar
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    
    and a target folder with its content will be created at the same level where it was executed (at same src folder level), with below content (as example):
    
    vagrant@jdriver:~/java$ ll target/
    total 28
    drwxrwxr-x 6 vagrant vagrant 4096 Oct  1 14:09 ./
    drwxrwxr-x 4 vagrant vagrant 4096 Oct  1 14:07 ../
    drwxrwxr-x 2 vagrant vagrant 4096 Oct  1 14:09 classes/
    drwxrwxr-x 3 vagrant vagrant 4096 Oct  1 14:09 generated-sources/
    -rw-rw-r-- 1 vagrant vagrant 3348 Oct  1 14:09 jdriver-1.0-SNAPSHOT.jar
    drwxrwxr-x 2 vagrant vagrant 4096 Oct  1 14:09 maven-archiver/
    drwxrwxr-x 3 vagrant vagrant 4096 Oct  1 10:32 maven-status/
    ```

9. Execute the jar file:

    ```
    $ java -jar target/jdriver-1.0-SNAPSHOT.jar 
    no main manifest attribute, in target/jdriver-1.0-SNAPSHOT.jar
    ```

    If you get above error, it is because the JAR file doesn’t know the entry point, so it has no idea where the main method is. Therefore, we can try with:

    A) Below command will compile and execute the java code:

    ```
    mvn compile exec:java -Dexec.mainClass="com.datastax.astra.jdriver"
    ```
    **NOTE**: NOT WORKING but maybe useful in the future...
    
    I tried with:
    
    ```
    $ mvn exec:exec -Dexec.executable="java" -Dexec.args="-classpath %classpath jdriver"
    [INFO] Scanning for projects...
    [INFO] 
    [INFO] ------------------------< org.example:jdriver >-------------------------
    [INFO] Building jdriver 1.0-SNAPSHOT
    [INFO]   from pom.xml
    [INFO] --------------------------------[ jar ]---------------------------------
    [INFO] 
    [INFO] --- exec:3.4.1:exec (default-cli) @ jdriver ---
    SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
    SLF4J: Defaulting to no-operation (NOP) logger implementation
    SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
    #############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################Cassandra version is: 4.0.0.6816
    #############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################[INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time:  25.288 s
    [INFO] Finished at: 2024-10-01T14:21:26Z
    [INFO] ------------------------------------------------------------------------
    ```
