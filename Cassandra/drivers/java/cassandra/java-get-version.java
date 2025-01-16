package com.datastax.oss;

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
