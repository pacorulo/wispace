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

5. Generate an Astra token
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

7. Create the java file (I named it `jdriver.java`) under previous folder 
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
    package com.datastax.astra;
    
    import com.datastax.oss.driver.api.core.CqlSession;
    import com.datastax.oss.driver.api.core.cql.ResultSet;
    import com.datastax.oss.driver.api.core.cql.Row;
    import java.nio.file.Paths;
    
    public class jdriver {
    
      public static void main(String[] args) {
    
        // The Session is what you use to execute queries. It is thread-safe and should be
        // reused
        try (CqlSession session = CqlSession.builder()
          .withCloudSecureConnectBundle(Paths.get("/path_to_scb/secure-connect-java.zip"))
          .withAuthCredentials("${clientid}","${token}")
          .build()) {
          // We use execute to send a query to Cassandra. This returns a ResultSet, which
          // is essentially a collection of Row objects
          ResultSet rs = session.execute("select release_version from system.local");
          //  Extract the first row (which is the only one in this case)
          Row row = rs.one();
    
          // Extract the value of the first (and only) column from the row
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

8. Almost done as we just have to execute mvn with the parameters/in the way:
   ```
   mvn compile exec:java -Dexec.mainClass="com.datastax.astra.jdriver"
   ```
