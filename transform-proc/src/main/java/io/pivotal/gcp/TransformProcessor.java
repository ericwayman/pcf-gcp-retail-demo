package io.pivotal.gcp;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import io.pivotal.gcp.domain.MockSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.stream.annotation.EnableBinding;
import org.springframework.cloud.stream.messaging.Processor;
import org.springframework.http.*;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@EnableBinding(Processor.class)
public class TransformProcessor {

    private final DateTimeFormatter dtFormat = DateTimeFormatter.ofPattern("MM/dd/yy HH:mm:ss");
    private LocalDateTime gcpNextDate;
    private ObjectMapper mapper;
    private String dsAppUrl;
    private boolean dsAppAvailable = true;

    @Autowired
    public TransformProcessor(
            @Value("${io.pivotal.gcp.gcp-next-date}") String nextDate,
            @Value("${io.pivotal.gcp.ds-app-09-url}") String dsAppUrl
    ) {
        gcpNextDate = LocalDateTime.from(dtFormat.parse(nextDate));
        this.dsAppUrl = dsAppUrl;
        mapper = new ObjectMapper();
        mapper.setPropertyNamingStrategy(PropertyNamingStrategy.SNAKE_CASE);
    }

    @ServiceActivator(inputChannel = Processor.INPUT, outputChannel = Processor.OUTPUT)
    public Object transform(Object payload) {
        System.out.println("TransformProcessor, payload => \"" + payload + "\"");
        try {
            // This shows how to deserialize the JSON into an Object
            MockSource mockSource = mapper.readValue(payload.toString(), MockSource.class);

            System.out.println("TransformProcessor, date-time => \"" + mockSource.getDateTime() + "\"");
            // dateTimeString is a String with this format: "02/21/17 14:13:33"
            LocalDateTime dateTime = LocalDateTime.from(dtFormat.parse(mockSource.getDateTime()));
            Duration deltaT = Duration.between(dateTime, gcpNextDate);
            //payload += " (" + deltaT.toDays() + " days 'til GCP NEXT)";
            mockSource.setDaysUntilMessage(deltaT.toDays() + " days 'til GCP NEXT");

            // This shows how to serialize that Object back to a JSON string
            payload = mapper.writeValueAsString(mockSource);

            // Here is how to POST this JSON to a REST API and receive the response
            payload = runDataScience(payload.toString());
        } catch (IOException e) {
            throw new ProcessorException(e);
        }
        System.out.println("TransformProcessor, transformed result => \"" + payload + "\"");
        return payload;
    }

    /**
     * Send the JSON object off to the Data Science Interrogator app and receive the JSON response.
     * If that service is not available, this is a no-op and returns the original JSON.
     */
    private String runDataScience(String json) {
        if (dsAppAvailable) {
            RestTemplate restTemplate = new RestTemplate();
            restTemplate.getMessageConverters().add(new MappingJackson2HttpMessageConverter());
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> entity = new HttpEntity<>(json, headers);
            try {
                ResponseEntity<String> response = restTemplate.exchange(dsAppUrl, HttpMethod.POST, entity, String.class);
                json = response.getBody();
            } catch (Exception e) {
                dsAppAvailable = false;
                System.out.println("Data Science App Unavailable at " + dsAppUrl);
            }
        }
        return json;
    }

}
