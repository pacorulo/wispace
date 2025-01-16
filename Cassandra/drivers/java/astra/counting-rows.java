package com.datastax.oss;

import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.ResultSet;
//import com.datastax.oss.driver.api.core.cql.Row;
import java.nio.file.Paths;


public class jdriver {
	
  public static void main(String[] args) {

    // The Session is what you use to execute queries. It is thread-safe and should be
    // reused.
    //try (CqlSession session = CqlSession.builder().build()) {
    try (CqlSession session = CqlSession.builder()
      //.withKeyspace(CqlIdentifier.fromCql("test"))
      .withCloudSecureConnectBundle(Paths.get("/home/pakete/vagrant/jdriver/secure-connect-java.zip"))
      .withAuthCredentials("${clientid}","${token}")
      .build()) {
      // We use execute to send a query to Cassandra. This returns a ResultSet, which
      // is essentially a collection of Row objects.
      session.execute("USE test");
      int number = 0;
      ResultSet rs1 = session.execute("select * from testing ALLOW FILTERING");
      ResultSet rs2 = session.execute("select count(*) from testing");

      System.out.println("###########################################################");
      System.out.println("####         Table test.testing content                ####");
      System.out.println("###########################################################");
      System.out.printf("Row %s%n is: %s%n",number, rs1.one().getFormattedContents());
      Long numberRows = rs2.one().getLong(0);

      for (int i = 1; i < numberRows; i++) {
	number++;
        System.out.println("###########################################################");
        System.out.printf("Row %s%n is: %s%n",number, rs1.one().getFormattedContents() );
      }
      System.out.println("###########################################################");
      System.out.println("###########################################################");
    }
  }
}
