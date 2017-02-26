package io.pivotal.gcp.domain;

/**
 * Base class for the various sources, for the Retail Demo
 */
public class RetailDemoSource {

    /**
     * Name of the source: facebook, twitter, instagram, snapchat, ...
     */
    private String source;

    public RetailDemoSource() {
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }
}
