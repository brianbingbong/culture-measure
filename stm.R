setwd("~/Documents/Projects/R-projects/culture-stm")

# Read in sample data
# google_doc_id <- "1LcX-JnpGB0lU1iDnXnxB6WFqBywUKpew" # google file ID
# poliblogs<-read.csv(sprintf("https://docs.google.com/uc?id=%s&export=download", google_doc_id), stringsAsFactors = FALSE)

# Read in review data
review_data = read.csv('./Dataset/Glassdoor_data/ericsson-filtered-joined.csv')
# review_data$rating_overall = as.factor(review_data$rating_overall)

# Load in stm
# install.packages('stm')
# install.packages('tm')
library(stm)

# Preprocess text to remove punc, stopwords, numbers and stemming
processed_reviews = textProcessor(review_data$review_text, metadata = review_data)

# remove common and rare terms
processed_reviews_out = prepDocuments(processed_reviews$documents, processed_reviews$vocab, processed_reviews$meta)
docs = processed_reviews_out$documents
vocab = processed_reviews_out$vocab
meta = processed_reviews_out$meta

# perform stm
reviews_stm = stm(documents = docs, vocab = vocab,
                  K = 12, prevalence =~ rating_overall,
                  max.em.its = 75, data = meta,
                  init.type = "Spectral", verbose = FALSE)

######### plot the stm
par(mfrow=c(1,1), oma=c(0,0,0,0))
plot(reviews_stm, main="Top 12 Topics Identified using STM on Ericsson Glassdoor Reviews")

######### plot all star charts
par(mfrow=c(2,6), oma=c(0,0,3,0))
plot(predict_topics, covariate = "rating_overall",
     topics = c(1), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 1",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(2), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 2",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(3), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 3",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(4), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 4",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(5), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 5",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(6), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 6",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(7), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 7",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(8), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 8",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(9), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 9",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(10), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 10",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(11), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 11",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
plot(predict_topics, covariate = "rating_overall",
     topics = c(12), 
     model = reviews_stm, method = "pointestimate",
     main = "Star Rating for Topic 12",
     xlim = c(0, 0.2), labeltype = "custom",
     custom.labels = c("5 stars", "4 stars", "3 stars", "2 stars", "1 stars"))
mtext("Relative Proportion of Ericsson Glassdoor Reviews pertaining to each Top 12 identified STM topic, Grouped by Star Rating", side=3, outer=TRUE, cex=1.5, line=-1 )

# extract some passages
findThoughts(reviews_stm, texts = review_data$review_text, n = 5, topics = 1)

# examine the effect of star ratings on topics
predict_topics<-estimateEffect(formula = 1:12 ~ rating_overall, stmobj = reviews_stm, metadata = meta, uncertainty = "Global")

summary(predict_topics, topics = 1, 2)

plot(predict_topics, covariate = "rating_overall",
     topics = c(2), 
     model = reviews_stm, method = "pointestimate",
     main = "Star rating for topic 2",
     xlim = c(0, 0.4), labeltype = "custom",
     custom.labels = c("5 star", "4 stars", "3 stars", "2 stars", "1 stars"))

predict_topic_single_t1 <- estimateEffect(formula = c(1) ~ rating_overall,
                                             stmobj = reviews_stm,
                                             metadata = meta,
                                             uncertainty="None")

predict_topic_single_t2 <- estimateEffect(formula = c(2) ~ rating_overall,
                                       stmobj = reviews_stm,
                                       metadata = meta,
                                       uncertainty="None")

predict_topic_single_t3 <- estimateEffect(formula = c(3) ~ rating_overall,
                                        stmobj = reviews_stm,
                                        metadata = meta,
                                        uncertainty="None")

predict_topic_single_t4 <- estimateEffect(formula = c(4) ~ rating_overall,
                                           stmobj = reviews_stm,
                                           metadata = meta,
                                           uncertainty="None")

predict_topic_single_t5 <- estimateEffect(formula = c(5) ~ rating_overall,
                                           stmobj = reviews_stm,
                                           metadata = meta,
                                           uncertainty="None")

predict_topic_single_t6 <- estimateEffect(formula = c(6) ~ rating_overall,
                                          stmobj = reviews_stm,
                                          metadata = meta,
                                          uncertainty="None")

predict_topic_single_t7 <- estimateEffect(formula = c(7) ~ rating_overall,
                                          stmobj = reviews_stm,
                                          metadata = meta,
                                          uncertainty="None")

predict_topic_single_t8 <- estimateEffect(formula = c(8) ~ rating_overall,
                                          stmobj = reviews_stm,
                                          metadata = meta,
                                          uncertainty="None")

predict_topic_single_t9 <- estimateEffect(formula = c(9) ~ rating_overall,
                                          stmobj = reviews_stm,
                                          metadata = meta,
                                          uncertainty="None")

predict_topic_single_t10 <- estimateEffect(formula = c(10) ~ rating_overall,
                                          stmobj = reviews_stm,
                                          metadata = meta,
                                          uncertainty="None")

predict_topic_single_t11 <- estimateEffect(formula = c(11) ~ rating_overall,
                                           stmobj = reviews_stm,
                                           metadata = meta,
                                           uncertainty="None")

predict_topic_single_t12 <- estimateEffect(formula = c(12) ~ rating_overall,
                                           stmobj = reviews_stm,
                                           metadata = meta,
                                           uncertainty="None")

plot(predict_topic_single_t5, 
     covariate = "rating_overall", 
     model = reviews_stm, 
     method = "continuous",
     xlab = "Rating", 
     linecol = "blue", 
     ylim = c(0, .20), 
     printlegend = F)

plot(predict_topic_single_t8, 
     covariate = "rating_overall", 
     model = reviews_stm, 
     method = "continuous",
     xlab = "Rating", 
     linecol = "red", 
     ylim = c(0, .20),
     add = T,
     printlegend = F)

plot(predict_topic_single_t10, 
     covariate = "rating_overall", 
     model = reviews_stm, 
     method = "continuous",
     xlab = "Rating", 
     linecol = "green", 
     ylim = c(0, .20),
     add = T,
     printlegend = F)

legend(4, 0.12, c("Topic 5", "Topic 8", "Topic 10"), lwd = 3, col = c("blue", "red", "green"))

plot(predict_topic_single_t2, 
     covariate = "rating_overall", 
     model = reviews_stm, 
     method = "continuous",
     xlab = "Rating", 
     linecol = "green", 
     ylim = c(0, .4),
     printlegend = F)
