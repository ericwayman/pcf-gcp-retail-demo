package io.pivotal.gcp.domain;

/**
 * Created by mgoddard on 2/24/17.
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
