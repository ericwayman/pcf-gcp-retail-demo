package io.pivotal.gcp;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.stream.annotation.EnableBinding;
import org.springframework.cloud.stream.messaging.Processor;
import org.springframework.integration.annotation.ServiceActivator;

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
        // payload is a String with this format: "02/21/17 14:13:33"
        LocalDateTime dateTime = LocalDateTime.from(dtFormat.parse(payload.toString()));
        Duration deltaT = Duration.between(dateTime, gcpNextDate);
        payload += " (" + deltaT.toDays() + " days 'til GCP NEXT)";
        //System.out.println("TransformProcessor, payload => \"" + payload + "\"");
        System.out.println(payload);
        return payload;
    }

}
