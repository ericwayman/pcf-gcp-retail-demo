# Mock Social Media Source for the Retail Demo

This is a little stand-in for future social media API adapters which will be
our data sources.

## For details on deploying this, running it, see the parent README
[Parent README](../README.md)

## Notable features
See the [code](./mock-source.py), where this object is constructed:

  `data = { 'date_time': d1.strftime('%m/%d/%y %I:%M:%S'), 'source': SOURCE_NAME }`

The idea is that each of the various sources will include a field, "source", which
indicates which source it's dealing with.  This could be used within the Java code
to indicated which class to map the incoming JSON data to, for deserialization.

