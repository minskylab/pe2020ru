import extractor
import counter
import drawer
import versions

text = extractor.extract_tweets_from_csv("file.csv")

freqs = counter.freq_str(text, minimal_counts=2)

drawer.draw_word_cloud(text)

sw = versions.StateWorker()
sw.save_new_snapshot()
sw.perform_generators()
