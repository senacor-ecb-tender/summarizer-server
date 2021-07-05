from summarizer.model import pre_process


def test_that_pipeline_is_functional():
    TEXT = """This box summarises the findings of an ad hoc ECB survey of leading euro area companies looking at the
impact that digitalisation has on the economy.[1] Digitalisation may be viewed as a technology/supply shock which 
affects the main economic aggregates, notably via competition, productivity and employment effects, as well as
through its interaction with institutions and governance. Digital technologies are also changing the ways in 
which firms do business and interact with their customers and suppliers. Understanding digital transformation 
and the channels through which it influences the economy is therefore increasingly relevant for the conduct of 
monetary policy. The main aim of the survey was to look at how digital transformation is affecting macroeconomic 
aggregates, as perceived by firms. The questionnaire asked companies about their take-up of digital technologies 
and the main obstacles to the adoption of such technologies. It then asked about the various channels through 
which they saw digital transformation affecting their sales, prices, productivity and employment, as well as the
expected overall direction and magnitude of the impact over the next three years. Responses were received from
74 leading non-financial companies, split equally between producers of goods and providers of services.
Those companies were generally very large, accounting for a combined total of around 3.7% of output and 1.7% 
of employment in the euro area. The take-up of digital technologies at those companies is very high, with big
data and cloud computing being the most widely adopted (see Chart A). The take-up of big data and cloud 
computing is pervasive across all sectors, as is the use of e-commerce, which is crucial in
business-to-consumer segments. In the manufacturing and energy sectors, artificial intelligence, the “internet
of things”, robotics and 3D printing are almost equally widespread, with respondents tending to report that the 
real impact comes when these technologies are combined. The main obstacles to the adoption of digital technologies
are the difficulty of adjusting the organisation of the company and the need to recruit and retain highly skilled
ICT staff. Regulation and legislation were not typically seen as a major obstacle, although some firms noted that,
while not a hindrance, regulatory frameworks did need to evolve.  Chart A Take-up of digital technologies and 
obstacles to their adoption  Take-up of digital technologies (percentages of respondents; responses ranked by 
overall rating)   Sources: ECB Digitalisation Survey and ECB calculations.Note: Based on responses to the following 
two questions: “Which digital technologies has your company adopted, including those you are in the process of 
adopting?” and “What are the main obstacles your company faced in relation to the adoption of digital technologies?”"""

    filtered_text = pre_process.filter_topic(TEXT, "pandemic", 3)

    assert len(filtered_text) < len(TEXT)


def test_that_sentences_with_keywords_are_kept():
    keywords = ["keyword", "relevant"]

    sentences = ["This sentence contains a Keyword.",
                 "This snippet of text does not.",
                 "Sometimes, multiple relevant keywords follow each other."]

    result = pre_process._extract_sentences_with_keywords(sentences, keywords)

    assert 0 in result
    assert 1 not in result
    assert 2 in result
