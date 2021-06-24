from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from model.summarize import predict

api = APIRouter()
templates = Jinja2Templates(directory="templates")


@api.get("/", response_class=HTMLResponse)
def index_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


short_summaries = {
    "climate_risk" : """
    Climate change provides us with an opportunity to rethink in order to broaden our horizons and
combine short-term, business-as-usual risk management tools with mechanisms that allow us
to better understand and manage risks driven by more structural, long-term changes in our
economies. What we want to safeguard is a resilient banking sector that prudently manages all risks, and
this clearly includes climate-related and environmental risks. To this end, on 20 May the ECB launched a public consultation on a draft guide on the
management and disclosure of climate-related and environmental risks. The guide describes how ECB Banking Supervision expects banks to consider, manage and
disclose climate-related and environmental risks in the light of current regulatory requirements. We will also continue to develop our supervisory approach to the management and disclosure
of climate-related and environmental risks. We can then also reap a double dividend: not only can we better safeguard the banking sector’s
resilience, but the adequate pricing of climate risks can drive a smoother and faster transition
to a more sustainable economy.
    """,
    "pandemic" : """First two phases of ECB Banking Supervision’s response to the pandemic: i) supervisory relief
and capital conservation and ii) assessing risks, vulnerabilities and the potential impact of the
pandemic on banks’ balance sheets (vulnerability analysis). ECB give banks capital and operational relief, but we also granted them temporary flexibility in
relation to the management of non-performing loans (NPLs), loan loss provisioning and loan
classifications. Our supervisory strategy, which is continuously adjusted to the challenges posed by the
pandemic, should serve as a catalyst for a stronger banking sector in the future. we plan to gradually intensify our scrutiny of banks’ preparedness to deal with the impending
deterioration in the quality of their assets (e.g. solid credit risk management practices and
prudent provisioning outcomes). Taking into account a further deterioration in asset quality, banks may need to take more
decisive action to reshape their business models (incl. ability to boost activities generating
non-interest income) and to tackle cost efficiency and transformation issues (e.g. teleworking). the COVID-19 pandemic should not be seen as an opportunity to question the validity of the
recently finalised international prudential framework, we need to maintain a longer-term view
and continue to strengthen our regulatory framework.""",
    "asset_quality": """The analysis of the potential vulnerabilities of the banking sector concluded that under the
central scenario the banking sector would be able to withstand the effects of the shock on its
asset quality but in a scenario with a sharper recession the deterioration of asset quality could
be significantly more material. This time the European banking sector entered the crisis in a much stronger position in terms
of the progress made in the last years on the asset quality side. The rise in the NPLs is expected but the crisis has so far not led to a noticeable increase in
non-performing loans. In the second quarter of 2020, the NPL ratio for significant institutions stood at 2.9%,
compared with 3.2% in the fourth quarter of 2019. If the suspension of payments was falling under these EBA recognised moratoria there
wouldn’t have been a need to automatically reclassify these loans as forborne, as
restructured. The data shows that, in the countries where the moratoria have already been lifted, most
customers of the banks have resumed payments as usual and only a fraction have shown
distress.""",
    "credit_lending" : """The relief measures activated by SSM could be used to finance up to EUR 1.8 trillion euro of
lending to households, small businesses and corporates during the COVID-19 pandemic. There might be a temptation to develop policies or national measures aimed at protecting local
establishments within countries and to unduly focus on the bank lending to national customers
only. As a result of the lending survey, in the first quarter of 2020, banks have tightened the lending
standards much less than they did in the first months of the financial crisis and the sovereign
debt crisis. As long as the new relief measures come into place, the banks expect to ease their lending
standards and accommodate the growing demand for loans that they see ahead of them. However, bank supervisors are not asking the banks to suspend their key function to assess
the credit worthiness of their counterparts when they lend. All the measures, especially for new lending, should be targeting valuable counterparts that
have a business future ahead of them."""}

long_summaries = {"climate_risk" : """The magnitude of climate-related risks for banks is likely to be significant. The effects of climate change unfold over a longer time horizon than the horizon usually taken
into account by investors, banks and policymakers. Climate change provides us with an opportunity to rethink in order to broaden our horizons and
combine short-term, business-as-usual risk management tools with mechanisms that allow us
to better understand and manage risks driven by more structural, long-term changes in our
economies. Although we don’t know exactly what level of transition and physical risks banks will face, we
do know that they will face some combination of these risks and that the risks will, in all
likelihood, worsen over time. In our view, it is therefore critical for banks to start developing their capacity to manage climate-
related and environmental risks. Adequately representing climate risks in banks’ balance sheets is a prerequisite not only for the
sector’s resilience, but also for the accurate pricing of these risks. And this, in turn, will contribute to an efficient and orderly transition to a low-carbon economy. What we want to safeguard is a resilient banking sector that prudently manages all risks, and
this clearly includes climate-related and environmental risks. To this end, on 20 May the ECB launched a public consultation on a draft guide on the
management and disclosure of climate-related and environmental risks. The guide describes how ECB Banking Supervision expects banks to consider, manage and
disclose climate-related and environmental risks in the light of current regulatory requirements. By doing so, we intend to provide transparency about the ECB’s understanding of safe and
prudent management of these risks within the current prudential framework, increase the
industry’s awareness of these risks and improve risk management practices. We will enter into a supervisory dialogue with banks as of next year in order to discuss practices
that diverge from our expectations and examine banks’ plans to address these gaps. We will also continue to develop our supervisory approach to the management and disclosure
of climate-related and environmental risks. As a prudential supervisor, we are and will remain dedicated to ensuring the resilience of banks,
which includes addressing these new sources of risk. We can then also reap a double dividend: not only can we better safeguard the banking sector’s
resilience, but the adequate pricing of climate risks can drive a smoother and faster transition
to a more sustainable economy.""",
                  "pandemic": """First two phases of ECB Banking Supervision’s response to the pandemic: i) supervisory relief
and capital conservation and ii) assessing risks, vulnerabilities and the potential impact of the
pandemic on banks’ balance sheets (vulnerability analysis). By releasing buffers and preventing capital from flowing out of the sector (i.e. refrain from
dividend distributions and share buy-backs), ECB helped to avert the sharp tightening of credit
standards that characterised the response to previous shocks. Not only did the ECB give banks capital and operational relief, but we also granted them
temporary flexibility in relation to the management of non-performing loans (NPLs), loan loss
provisioning and loan classifications. In a letter to banks in July, ECB asked the sector to focus more on proactively identifying
distressed borrowers and managing deteriorating assets at an early stage and ECB also
extended the blanket recommendation that banks should refrain from dividend distributions. Our supervisory strategy, which is continuously adjusted to the challenges posed by the
pandemic, should serve as a catalyst for a stronger banking sector in the future. On the one hand, it is time for banks to brace for the impact that will likely materialise as the
system-wide moratoria are lifted. On the other hand, a proactive attitude is needed on all sides for the pandemic not to act as a
mere amplifier of long-lasting and well-known structural deficiencies. European banking sector was already suffering from several structural weaknesses (e.g.
persistent low profitability, caused by excess capacity and low cost efficiency) which has
driven bank valuations to historic lows. The sooner NPLs are identified and provisioned for, the faster and smoother the NPL
resolution and disposal process will be, averting damaging hangover effects down the road. we plan to gradually intensify our scrutiny of banks’ preparedness to deal with the impending
deterioration in the quality of their assets (e.g. solid credit risk management practices and
prudent provisioning outcomes). A clearer picture on the trajectory of asset quality will also be needed to inform our review of
the recommendation to suspend dividend payments, which we will complete in December. Taking into account a further deterioration in asset quality, banks may need to take more
decisive action to reshape their business models (incl. ability to boost activities generating
non-interest income) and to tackle cost efficiency and transformation issues (e.g. teleworking). In this quest to restore profitability, banks should also consider the possible benefits of
business combinations. the COVID-19 pandemic should not be seen as an opportunity to question the validity of the
recently finalised international prudential framework, we need to maintain a longer-term view
and continue to strengthen our regulatory framework.""",
                  "asset_quality": """Asset long summary not available""",
                  "credit_lending": """Credit lending long summary not available"""}


@api.post("/upload")
async def upload_file(request: Request,
                topic=Form(...),
                summary_type=Form(...),
                file: UploadFile = File(None) #TODO: make not optional
                ):
    result = short_summaries[topic] if summary_type == 'short' else long_summaries[topic]
    print('received call')
    if file is not None:
        content = (await file.read()).decode('utf-8')
        result = predict(content, topic, summary_type)

    return {"result": result}

    #return templates.TemplateResponse("index.html", {"request": request, "result": result})
