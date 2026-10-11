# Calendar export sketch

Action items already carry {owner, text, source_segment}. An `.ics` writer
could emit one VEVENT per item, with the segment link in the description.

No changes to the report schema - the export is a side artifact, and the
option stays off by default.
