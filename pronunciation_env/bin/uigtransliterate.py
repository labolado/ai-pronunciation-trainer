#!/Users/yee/data/dev/app/ai/my_stories/AI/app/跟读/ai-pronunciation-trainer/pronunciation_env/bin/python
from __future__ import print_function

import fileinput
import epitran

epi = epitran.Epitran('uig-Arab')
for line in fileinput.input():
    s = epi.transliterate(line.strip().decode('utf-8'))
    print(s.encode('utf-8'))
