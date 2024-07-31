## Dashboard Configuration

### Global Settings
- **Global Filter**: 
  - **Year**: Filter by specific years from 2010-2016.

### Visualizations

#### New Hires Summary
- **Type**: Card
- **Task**: Summarize
- **Description**: This card summarizes the current value of New Hires.
- **Title**: New Hires

#### New Hires SPLY Summary
- **Type**: Card
- **Task**: Summarize
- **Description**: This card summarizes the current value of New Hires for the same period last year (SPLY).
- **Title**: New Hires SPLY

#### Region Filter
- **Type**: Filter
- **Task**: Discover, derive, explore
- **Description**: This filter allows users to filter data by Region. There are seven regions: North, Midwest, Nortwest, East, Central, South, West
- **Interactions**: 
  - Clicking on a value filters the report by Region.
  - Affects multiple charts including New Hires, New Hires SPLY, New Hires and Same Period Last Year, New Hires by Month and FPDesc, and New Hires by Region and Ethnicity.

#### Ethnicity Filter
- **Type**: Filter
- **Task**: Discover, derive, explore
- **Description**: This filter allows users to filter data by Ethnicity. There are seven ethnicity groups: Group A - Group G
- **Interactions**: 
  - Clicking on a value filters the report by Ethnicity.
  - Affects multiple charts including New Hires, New Hires SPLY, New Hires and Same Period Last Year, New Hires by Month and FPDesc, and New Hires by Region and Ethnicity.

#### New Hires by Month and FPDesc
- **Type**: Line Chart
- **Task**: Show trend
- **Description**: This line chart displays trends in New Hires over months, categorized by full- and part time hires (FPDesc). The X-axis represents the months for a full year, and the Y-axis represents the number of New Hires. Different FPDesc categories are distinguished by color.
- **Title**: New Hires by Month and FPDesc
- **Interactions**: 
  - Clicking on a line filters the report by Month.
  - Hovering over a line provides detailed information.
  - Clicking on axis labels or legend filters the report by Month or FPDesc.

#### New Hires by Region
- **Type**: Clustered Bar Chart
- **Task**: Part-to-whole relationship, lookup values, find trends
- **Description**: This chart uses bars to compare and find trends in New Hires across regions. The X-axis represents the number of new hires, and the Y-axis represents different regions. 
- **Title**: New Hires by Region
- **Interactions**: 
  - Clicking on a bar filters the report by the corresponding Region.
  - Hovering over elements provides detailed information.

#### New Hires by Ethnicity
- **Type**: Clustered Bar Chart
- **Task**: Part-to-whole relationship, lookup values, find trends
- **Description**: This chart uses bars to compare and find trends in New Hires across ethnicities. There are seven ethnicity groups: Group A - Group G. The X-axis represents the number of new hires, and the Y-axis represents different ethnicities. 
- **Title**: New Hires by Ethnicity
- **Interactions**: 
  - Clicking on a bar filters the report by the corresponding Ethnicity.
  - Hovering over elements provides detailed information.

#### New Hires and New Hires Same Period Last Year
- **Type**: Clustered Column Chart
- **Task**: Compare, lookup values, find trends
- **Description**: This chart compares New Hires and New Hires for the same period last year. It uses bars to show trends over time. It shows the sum of full- and part time new hires for every month. The X-axis represents the months for a whole year and the Y-axis represents the total amount of new hires. 
- **Title**: New Hires and New Hires Same Period Last Year
- **Interactions**: 
  - Clicking on elements filters the report by Month.
  - Hovering over elements provides detailed information.
  - Clicking on labels or legends filters the report by Month, New Hires, or New Hires SPLY.