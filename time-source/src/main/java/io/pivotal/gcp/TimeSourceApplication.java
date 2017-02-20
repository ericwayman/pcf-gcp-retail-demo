package io.pivotal.gcp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Import;

@SpringBootApplication
@Import(org.springframework.cloud.stream.app.time.source.TimeSourceConfiguration.class)
public class TimeSourceApplication {

	public static void main(String[] args) {
		SpringApplication.run(TimeSourceApplication.class, args);
	}

}
