from report_page_integration import *
#The following commented out parameterizations can be used to run unique tests, however,
#I have only a day later completing this realize that only the shown to create any unique output
#This reduces test cases from 72 -> 8
@pytest.mark.parametrize("gen_recommendations", [True]) #[True, False])
@pytest.mark.parametrize("annual_revenue_million", [1.1, 2.1, 4.1, 7.1])
@pytest.mark.parametrize("industry_id", [0, 3, 4])
@pytest.mark.parametrize("orientation", ["Horizontal"])#["Horizontal", "Vertical"])
@pytest.mark.parametrize("saas_type_id", [0, 1]) #[0, 1, 2])
#Individual Tests if needed
# @pytest.mark.parametrize("saas_type_id, orientation, industry_id, annual_revenue_million, gen_recommendations", [
#     (0, "Horizontal", 0, 1.1, True)
# ])
def test_generate_report(saas_type_id, orientation, industry_id, annual_revenue_million, gen_recommendations):
    report_generator(saas_type_id, orientation, industry_id, annual_revenue_million, gen_recommendations)