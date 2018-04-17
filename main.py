__author__ = '得一'

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scarpy", "crawl", "ishare"])
# execute(["scarpy", "crawl", "pipipan"])
execute(["scarpy", "crawl", "mebook"])