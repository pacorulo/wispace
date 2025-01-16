package com.datastax.oss;

import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.ResultSet;
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
      session.execute("USE test");
      int row_number = 0;
      ResultSet rs1 = session.execute("select * from testing ALLOW FILTERING");
      ResultSet rs2 = session.execute("select count(*) from testing");

      System.out.println("###########################################################");
      System.out.println("####         Table test.testing content                ####");
      System.out.println("###########################################################");
      System.out.printf("Row %s%n is: %s%n",row_number, rs1.one().getFormattedContents());
      Long totalRows = rs2.one().getLong(0);

      for (int i = 1; i < totalRows; i++) {
	row_number++;
        System.out.println("###########################################################");
        System.out.printf("Row %s%n is: %s%n",number, rs1.one().getFormattedContents() );
      }
      System.out.println("###########################################################");
      System.out.println("###########################################################");
    }
  }
}
