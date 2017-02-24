package io.pivotal.gcp.domain;

/**
 * Mock social media source to correspond with the mock-source Python app
 */
public class MockSource extends RetailDemoSource {

    private String dateTime;
    private String daysUntilMessage;

    // Required for Jackson to work
    public MockSource() {
        super();
    }

    public String getDateTime() {
        return dateTime;
    }

    public void setDateTime(String dateTime) {
        this.dateTime = dateTime;
    }

    public String getDaysUntilMessage() {
        return daysUntilMessage;
    }

    public void setDaysUntilMessage(String daysUntilMessage) {
        this.daysUntilMessage = daysUntilMessage;
    }
}
