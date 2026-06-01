As a library admin I want to automaticvally ingest and clean the flat files I manually curate each day to impress my boss.

# How would I do it?

Stage 1 : ingestion
    - Needs a trigger/schedule
    - possible matching issues depenedant on src location
    - 1 master script or 1 for each type

Stage 2 : clean
    - Need to ID issues
    - Prepare for dirty dates, duplicates and text character errors
    - log all fixes and counts

Stage 3 : Store
    - Store outputs in DB
    - aggreagte fixes, create output of impacts / success/ fails etc


In addition:
    - Log activity at each stage
    - Add logs to a DB for visualisation

To consider:
    - no current DE systems, new services will be expensive 
    - small bespoke management via scripts be cheaper but will add technical debt
 
    
![Rough Process Map](image.png)