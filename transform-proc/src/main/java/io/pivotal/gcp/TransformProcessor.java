package io.pivotal.gcp;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import io.pivotal.gcp.domain.MockSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.stream.annotation.EnableBinding;
import org.springframework.cloud.stream.messaging.Processor;
import org.springframework.integration.annotation.ServiceActivator;

import java.io.IOException;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@EnableBinding(Processor.class)
public class TransformProcessor {

    private final DateTimeFormatter dtFormat = DateTimeFormatter.ofPattern("MM/dd/yy HH:mm:ss");
    private LocalDateTime gcpNextDate;

    @Autowired
    public TransformProcessor (@Value("${io.pivotal.gcp.gcp-next-date}") String nextDate) {
        gcpNextDate = LocalDateTime.from(dtFormat.parse(nextDate));
    }

    @ServiceActivator(inputChannel = Processor.INPUT, outputChannel = Processor.OUTPUT)
    public Object transform(Object payload) {
        System.out.println("TransformProcessor, payload => \"" + payload + "\"");
        ObjectMapper mapper = new ObjectMapper();
        mapper.setPropertyNamingStrategy(PropertyNamingStrategy.SNAKE_CASE);
        try {
            MockSource mockSource = mapper.readValue(payload.toString(), MockSource.class);
            System.out.println("TransformProcessor, date-time => \"" + mockSource.getDateTime() + "\"");
            // dateTimeString is a String with this format: "02/21/17 14:13:33"
            LocalDateTime dateTime = LocalDateTime.from(dtFormat.parse(mockSource.getDateTime()));
            Duration deltaT = Duration.between(dateTime, gcpNextDate);
            //payload += " (" + deltaT.toDays() + " days 'til GCP NEXT)";
            mockSource.setDaysUntilMessage(deltaT.toDays() + " days 'til GCP NEXT");
            payload = mapper.writeValueAsString(mockSource);
        } catch (IOException e) {
            throw new ProcessorException(e);
        }
        System.out.println("TransformProcessor, transformed result => \"" + payload + "\"");
        return payload;
    }

}
