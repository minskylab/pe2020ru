import extractor
import counter
import drawer
import worker

text = extractor.extract_tweets_from_csv("file.csv")

freqs = counter.freq_str(text, minimal_counts=2)

drawer.draw_word_cloud(text)

# sw = versions.GovernmentWorker()
# sw.save_new_snapshot()
# sw.perform_generators()
