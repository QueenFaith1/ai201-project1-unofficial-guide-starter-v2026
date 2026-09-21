Chunk 1 - source: thread_bike_commute.txt#0 | produced by: chunker.py::split_documents

THREAD: Is a bike worth it for a 20 minute walk commute?

 reply 1 (14 votes) 
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage, covered bike parking exists at three buildings and is full by 9am at all three.

Chunk 2 - source: thread_first_gen.txt#1 
produced by: chunker.py::split_documents

THREAD: Anything specific for first-generation students?

reply 2 (41 votes) 
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

Chunk 3,  source: thread_laptop_specs.txt#2  produced by: chunker.py::split_documents

THREAD: How much laptop do I actually need for CS courses?

reply 3 (12 votes) 
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.

Chunk 4, source: thread_parking.txt#1 | produced by: chunker.py::split_documents

THREAD: Worth getting a parking permit?

 reply 2 (21 votes) 
Street parking on Verrill is legal and free and unmarked, which is why half the upper years do it.

Chunk 5,  source: thread_sleep_schedule.txt#1  produced by: chunker.py::split_documents

THREAD: Everyone says fix your sleep. Does it actually matter?

 reply 2 (37 votes) 
The library being open until 2am is a trap. It's a resource, not a schedule.

## Chunking Strategy

**Chunk size:** I didn't use a fixed size. My chunker splits documents wherever a reply starts, so chunk size depends on how long each reply happens to be.

**Overlap:** None. Each reply becomes its own separate chunk, so nothing repeats between them.

When I ran the original chunker on my corpus, it printed a chunk that was only 2 characters long, basically a broken fragment with nothing useful in it. My corpus is made of threads where each post follows the same pattern: a thread title, then several replies marked like "--- reply 1 (14 votes) ---". Since that structure was already there in the text, I split at those reply markers instead of guessing at a character count. Each chunk keeps the thread title attached so it still makes sense on its own, without needing the other replies around it.