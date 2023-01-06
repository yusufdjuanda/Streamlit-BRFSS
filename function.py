# Function compilation

import streamlit as st # To utilize streamlit method
import pandas as pd 
import plotly.express as px # To produce a simple interactive graph
from plotly.subplots import make_subplots # Advance customization of the graph
from streamlit_lottie import st_lottie # To add the moving icon
import scipy.stats as stats # To perform a statistics test

# Integrating all the streamlit component in function


# Function to run a streamlit component in the main page section 
def main_page():
    
    main_page = st.container() # Creating a container so anything that starts with 'main_page' will be included in the container 
    main_page.title("About the Project")

    main_page.markdown("""
    The project is part of the final presentation of _Basic Programming Class_ Fall 2022 from **Taipei Medical University.**
    """)
    main_page.markdown("""---""")
    main_page.subheader("Dataset")
    main_page.markdown("""
    The Behavioral Risk Factor Surveillance System (BRFSS) was assigned to us to perform further analysis.
    """)
    main_page.markdown("""---""")
    main_page.subheader("Objectives")
    main_page.markdown("""
    1. To perform Exploratory Data Analysis (EDA) on the BRFSS dataset and to have an overview of the content.
    2. To explore further about the smoking status frequency distribution based on different group population.
    """)
    main_page.markdown("""---""")
    main_page.subheader("Group 3")
    main_page.markdown("""
    - Yusuf Maulana - M610111010
    - Lutvi Vitria Kadarwati - M850111006
    - Harold Arnold Chinyama  - M610111011
    """)
    main_page.markdown("""---""")
    main_page.write("Should you have any feedback or questions, please contact m610111010@tmu.edu.tw")

    return main_page

# Function to run a streamlit component in the brfss page section  
def brfss_page(display_df, transformed_df, loc_df, lottie_json):
    brfss_page = st.container()
    brfss_page.title("The Behavioral Risk Factor Surveillance System (BRFSS)")

    brfss_page.markdown("""
    **BRFSS** is the nation’s premier system of health-related telephone surveys that collect state data about U.S. residents regarding their health-related risk behaviors, chronic health conditions, and use of preventive services.
    For more information, visit https://www.cdc.gov/brfss.
    """
    )
    # Dividing the page into 3 tabs 
    tab1, tab2, tab3 = brfss_page.tabs(["Dataset", "Data Transformation","Topics"])
    with tab1: #Indented codes will be run under the tab1
        st.subheader("Dataset")
        st.markdown(
            "The dataset was provided to us via **Google Drive** and for learning purpose, the original dataset was utilized for further analysis."
        )
        st.markdown('\n')

        display = st.container()
        display.write("**Glance of the first 20 rows of the dataset**")
        display.dataframe(display_df.head(20))
        display.markdown(
            """
        _There are **2.048.467** observations and **27** variables_
        """
        )
        with st.expander("See important variables"): # Streamlit function for containing components inside of the expander
            st.caption(
                """
                1. **Year**: The year of the survey was conducted
                2. **Location**: States in the USA
                3. **Class**: Class of the topic
                3. **Topic**: Topics of the survey which lead specific questions and responses 
                4. **Question**: The question used for the survey
                5. **Response**: The response from the respondents
                6. **Break_Out**:  Group category of the respondents, which later will be renamed to "Category"
                7. **Break_Out_Category**: Class of the group category, which later will be renamed to "Class_Category"
                8. **Sample_Size**: Number of respondents
            """
            )

    with tab2: #Indented codes will be run under the tab2
        st.subheader("Transformed Dataset")
        st.markdown("""
        From the original dataset, (Exploratory Data Analysis) EDA was performed to produce 2 transformed datasets with some additional variables.
        - General dataset
        - Location dataset for smoking status
        """)
        radio = st.radio('Select the transformed dataset', ['General dataset','Location dataset'], horizontal = True) # radio selection
        if radio == "General dataset": # If the 'General dataset' is chosen the following codes will be executed
            st.dataframe(transformed_df.head(20))
            st.write("_There are **3.8142** observations and **10** variables_")
            st.markdown("""
            **Additional variables**
            - Percentage : Relative frequency of the sample size from each response per number of respondents in every question or topic in the specific year e.g., frequency of male smokers in 2011 is male respondents that are smokers among the total male respondents in the \'smokers status\' topic in 2011
            Percentage = sample size / total sample size 
            - Total_SS : Total respondents of specific question in specific year from specific group category.

            """)
        
        else:
            st.dataframe(loc_df.head(20))
            st.write("_There are **1.060** observations and **8** variables_")
            st.markdown("""
            **Additional variables**
            - Percentage_Loc : Relative frequency of the sample size from smoking status response per number of respondents in every location or topic in the specific year 
            Percentage = sample size / total sample size 
            - Total_SS_Loc : Total respondents of specific location in specific year
            - latitude / longitude = Coordinates obtained from 'Geolocation' column

            """)
    #Indented codes will be run under the tab3
    with tab3:
        
        st_lottie(lottie_json, width = 100, height = 100)
        st.title("Topics Covered")
        st.markdown("""---""")

        st.markdown(f"""
        Based on the given dataset, there are **{len(transformed_df['Topic'].unique())}** different topics inquired during the BRFSS survey. 
        The number of questions may vary in accordance with the topic. The type of questions are open-ended which lead to simple categorical responses.
        \n
        This page provides an overview of the response rate from every question with the corresponding year of the survey conducted.
        - Donut graph: Providing a proportion of the responses on the selected question in the selected year.
        - Line graph: Providing an information of responses on the selected question from 2011 to 2020.
        
        """)

        st.markdown("""---""")

        graph = st.radio("Select the graph", ["Donut graph","Line graph"], horizontal = True)

        col3, col4 = st.columns(2)

        with col3:
            chosen_topic = st.selectbox(
                "Select Topic",
                transformed_df["Topic"].sort_values().value_counts().sort_index().index.tolist(),
            ) 
            question = st.radio('Select Question(s)', transformed_df["Question"].loc[transformed_df["Topic"] == chosen_topic].unique())

        if graph == 'Donut graph':
            with col4:
                # Load the dataframe to match with specific question and year
                year = st.selectbox('Select year', transformed_df["Year"].loc[transformed_df["Topic"] == chosen_topic].unique())

                df_response = transformed_df.loc[(transformed_df['Class_Category'] == "Overall") & (transformed_df['Question'] == question)  & (transformed_df['Year'] == year)].groupby(['Response','Year', 'Sample_Size', 'Total_SS'])['Percentage'].sum().reset_index()
                df_response['mid'] = 'Response' # adding one column containing string 'Response' to appear in the middle of pie chart
                fig = px.sunburst(
                            df_response,
                            path=["mid", "Response", "Percentage"],
                            values="Percentage",
                            color_discrete_sequence=px.colors.qualitative.Set2,
                            maxdepth = 2,
                            title = "Responses",
                            hover_data= {
                                'Sample_Size': True,
                                'Total_SS': True
                            }
                        ).update_traces(insidetextorientation='auto')
                # with col4:
                st.plotly_chart(fig, use_container_width= True)

        if graph == 'Line graph':
            df_response = transformed_df.loc[(transformed_df['Class_Category'] == "Overall") & (transformed_df['Question'] == question)].groupby(['Year','Response','Sample_Size', 'Total_SS'])['Percentage'].sum().reset_index()
            fig = px.line(
                df_response, x="Year", y="Percentage", color="Response", template="seaborn", width=700, height=400,
                hover_data=['Percentage', 'Sample_Size', 'Total_SS', 'Year'],
            )
            st.write(f"**{question}**")
            st.plotly_chart(fig, use_container_width=True)

        with st.expander("See group category"):

            sunburst_df = (
            transformed_df.groupby(["Class_Category", "Category"])["Total_SS"].sum().reset_index()
            )
            sunburst_df = sunburst_df.replace(["Education Attained", "Household Income"], ["Education", "Income"])
            sunburst_df["mid"] = "Category" # adding one column containing string 'Category' to appear in the middle of pie chart

            # to make 2 containers
            col1, col2 = st.columns([1,2])

            with col1:
                st.subheader("Group Category")
                st.write(
                    "There are 6 unique group categories representing the additional information of the respondents."
                )

            with col2:
                fig = px.sunburst(
                    sunburst_df.loc[sunburst_df["Total_SS"] > 10000000],
                    path=["mid", "Class_Category", "Category"],
                    values="Total_SS",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    maxdepth = 2
                ).update_traces(insidetextorientation='auto')
                
                st.plotly_chart(fig, use_container_width=True)

# Function to run a streamlit component in the smoking status page 
def smoking_page(df_smokers, loc_df):
    smoking_page = st.container()
    smoking_page.title("Smoking Status")
    smoking_page.markdown("""---""")

    smoking_page.markdown("""
    One aspect of the BRFSS survey is to collect data on smoking status. 
    This page provides an overview of smoking prevalence among adults in the United States over the past decade, broken down by various demographic categories.\n
    The filters provided can be used to further explore smoking prevalence among different population groups, such as by gender, age, race/ethnicity, education level, and income. 
    This information can be used to better understand the factors that contribute to smoking behavior.
    """)


    smoking_page.subheader("Data Visualization")
    tab1, tab2 = smoking_page.tabs(["Group Category", "Location"]) # Dividing into 2 tabs

    with tab1:
        st.subheader("Smokers Distribution Based on The Group Category")

        st.write("""
        The relative frequency is represented by the percentage which is based on the sum of each group category of respondents in the year of BRFSS Survey. \n
        e.g., frequency of male smokers in 2011 is male respondents that are smokers among the total male respondents in the \'smokers status\' topic in 2011.
        - Line graph: Providing an information of the smokers rate of the selected group category from 2011 to 2020.
        - Bar graph: Providing an information of the smokers rate of the selected group category in the selected year.
        """)

        col5, col6 = st.columns(2) # make 2 columns for selectbox
        with col5:
            group_cat = st.selectbox(
                "Group category",
                [
                    "Overall",
                    "Age Group",
                    "Education Attained",
                    "Race/Ethnicity",
                    "Gender",
                    "Household Income"
                    
                ],
            )

        radio = st.radio('Select the graph', ['Line graph','Bar graph'], horizontal = True) # selection for type of graph

        df_smokers = df_smokers[df_smokers['Topic'] == 'Smoker Status']
        # Specifying df_smokers according to the group category
        df_cat = df_smokers[df_smokers.Class_Category == group_cat]
        data_plotly = df_cat[(df_cat.Response == "Yes")]

        
        # Condition if the Line graph is selected produce the line graph, else produce the bar graph
        if radio == 'Line graph':

            fig = px.line(
                data_plotly, x="Year", y="Percentage", color="Category", template="seaborn", width=700, height=400,
                title=f"Frequency distribution of smokers in the USA across the {group_cat}",
                hover_data=['Percentage', 'Sample_Size', 'Total_SS', 'Year'],
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            with col6: # the second column will only appear if 'Line graph' is chosen
                year1 = st.selectbox("Year", df_smokers["Year"].unique())

            if group_cat == "Overall":
                st.write(f"**Frequency distribution of smokers in the USA across the {group_cat} in {year1}**")
                fig = px.bar(data_plotly[data_plotly['Year'] == year1], x="Category", y="Percentage", template = "seaborn", text_auto= True, width = 200, hover_data=['Percentage', 'Sample_Size', 'Total_SS', 'Year'])
                st.plotly_chart(fig)
            else:
                st.plotly_chart(fig)
            
    
    with tab2:

        st.subheader("Smokers Distribution Based on The Location")
        st.markdown("""
        Frequency distribution of smokers across the USA states ranked by the highest or the lowest or lowest smokers prevalence.
        - Bar graph: Providing an information of the smokers rate of the location in the selected year.
        - Line graph: Providing an information of the smokers rate of the selected location from 2011 to 2020.
        
        """)
        st.write("\n\n\n")

        graph = st.radio("Select the graph", ['Bar graph', 'Line graph'], horizontal = True)
        if graph  == 'Bar graph':
            col1, col2, col3 = st.columns(3)
            with col1:
                year = st.selectbox("Select year", loc_df["Year"].unique())
            with col2:
                states = st.selectbox("Number of states", [3,5,10])
            with col3:
                rank = st.selectbox("Sort the frequency by", ["Lowest", "Highest"] )

            sorting = rank == "Lowest"

            df_loc = loc_df.loc[loc_df['Response'] == 'Yes']
            df_loc = df_loc[df_loc["Year"] == year].sort_values(by = 'Percentage_Loc', ascending = sorting).reset_index().head(states)
            subplots = create_bar_chart(df_loc)
            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(subplots, use_container_width= True)

            with col4:
                c = st.container()
                map = c.expander("See Map")
                with map:
                    st.map(df_loc, zoom = 0.7, use_container_width = True)

        if graph == 'Line graph':
            
            states = st.multiselect('Select the states', loc_df['Locationdesc'].unique(), ['West Virginia','Guam','Kentucky'])
            df_loc = loc_df.loc[(loc_df['Locationdesc'].isin(states)) & (loc_df['Response'] == 'Yes')]
            df_loc = df_loc.groupby(['Year','Locationdesc','Sample_Size','Total_SS_Loc', 'latitude', 'longitude'])['Percentage_Loc'].sum().reset_index()
            
            fig = px.line(
                df_loc, x="Year", y="Percentage_Loc", color="Locationdesc", template="seaborn", width=700, height=400,
                hover_data=['Percentage_Loc', 'Sample_Size', 'Total_SS_Loc', 'Year'],
            )
            st.plotly_chart(fig, use_container_width=True)
            
            map = st.expander("See Map")
            with map:
                st.map(df_loc, zoom = 0.7, use_container_width = True)

    st.markdown("---")
    st.subheader("Conclusion")
        
    st.markdown("""
    According to the most recent data from the BRFSS, the prevalence of smoking among adults in the United States is approximately **14%** in 2020. 
    This means that about 1 in 8 adults in the country are current smokers. 
    However, as shown in the graph, there is significant variation in smoking rates among different population groups.\n
    
    Chi-square test of independence is used to determine if there is a significant association between smoking status and group category as well as the location.
    All the group category has shown a significant association with the smoker status (p<0.05) which indicates the smoking status rate is influenced by the population groups
    such as age group, education level, race/ethnicity, gender, household income, and location.
    """)

    
    # Loading dataframe for crosstab based on group category
    df_statistics = df_smokers
    df_statistics = df_statistics[df_statistics['Topic'] == 'Smoker Status']
    df_statistics = df_statistics.groupby(['Class_Category', 'Category', 'Response'])['Sample_Size'].sum().reset_index()
    
    # Loading dataframe for crosstab based on the location
    df_stat_loc = loc_df.groupby(['Locationdesc', 'Response'])['Sample_Size'].sum().reset_index()

    statistics = st.expander("See chi-square results")

    with statistics:
        st.write("Cumulative sum of the sample size from 2011 - 2020 is used to calculate the chi-square test")

        group_cat = st.selectbox("Select group category", [
                                'Age Group', 'Education Attained', 'Gender', 'Household Income', 'Race/Ethnicity', 'Location'])

        
        if group_cat == 'Location':

            crosstab = pd.crosstab(index = df_stat_loc.Locationdesc, columns = df_stat_loc.Response,
                                values = df_stat_loc.Sample_Size, aggfunc = sum, margins = True)

            # Perform chi-square test

            stat, p, dof, expected = stats.chi2_contingency(crosstab)

            st.write("Chi-square statistic: {:.3f}".format(stat))
            st.write("p-value: {:.3f}".format(p))
            st.write("Degrees of freedom: {:.0f}".format(dof))

        else:

            df_statistics = df_statistics[(df_statistics['Class_Category'] == group_cat)]
            crosstab = pd.crosstab(index=df_statistics.Category, columns=df_statistics.Response,
                                values=df_statistics.Sample_Size, aggfunc=sum, margins=True)

            # Perform chi-square test
            stat, p, dof, expected = stats.chi2_contingency(crosstab)

            st.write("Chi-square statistic: {:.3f}".format(stat))
            st.write("p-value: {:.3f}".format(p))
            st.write("Degrees of freedom: {:.0f}".format(dof))
    st.markdown("---")

    return smoking_page


def create_bar_chart(df_loc): # Advance vertical bar plotting using subplots on plotly
    subplots = make_subplots(
            rows= len(df_loc),
            cols=1,
            subplot_titles=[x for x in df_loc['Locationdesc']],
            shared_xaxes=True,
            print_grid=False,
            vertical_spacing=(0.45 / len(df_loc)),
        )

    for i, j in df_loc.iterrows():
        subplots.add_trace(dict(
            type='bar',
            orientation='h',
            y=[j["Locationdesc"]],
            x=[j["Percentage_Loc"]],
            text=[f'{j["Percentage_Loc"]}%'],
            hoverinfo='text',
            textposition='auto',
            marker=dict(
                color = [j["Percentage_Loc"]],
                colorscale = "purples",
            ),
        ), i+1, 1)

    subplots['layout'].update(
        showlegend=False,
    )
    _ = subplots['layout'].update(
        width=550,
    )
    for x in subplots["layout"]['annotations']:
        x['x'] = 0
        x['xanchor'] = 'left'
        x['align'] = 'left'
        x['font'] = dict(
            size=15,
        )
    for axis in subplots['layout']:
        if axis.startswith('yaxis') or axis.startswith('xaxis'):
            subplots['layout'][axis]['visible'] = False

    subplots['layout']['margin'] = {
        'l': 0,
        'r': 0,
        't': 20,
        'b': 1,
    }
    height_calc = 45 * len(df_loc)
    height_calc = max([height_calc, 350])
    subplots['layout']['height'] = height_calc
    subplots['layout']['width'] = height_calc
        
    return subplots
        


        


