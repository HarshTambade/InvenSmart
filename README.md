Here's a `README.md` file for your project:

---

# InvenSmart India Dashboard

InvenSmart is an AI-powered hyperlocal inventory management solution designed to provide real-time insights into sales, stock levels, and inventory optimization. This platform focuses on efficient demand prediction, inventory optimization, and data-driven recommendations for retailers across India.

## Project Overview

The **InvenSmart India Dashboard** application is a Streamlit-based web app that visualizes inventory data, provides key insights, and offers recommendations for improving inventory and sales management. This project incorporates dynamic data filtering, AI-based sales trends, and insights into a visually engaging dashboard.

## Features

- **Dynamic Sales Insights**: Get an overview of sales trends, category-wise performance, and location-based analysis.
- **Map Visualization**: Visualize store locations across India with sales and stock levels displayed on an interactive map.
- **AI-Based Recommendations**: Inventory and restocking recommendations based on key performance metrics.
- **Analytics Dashboard**: Explore detailed analytics on sales trends, category distribution, and top-performing locations and products.
- **Date and Category Filters**: Filter data based on selected date ranges and product categories.

## Getting Started

### Prerequisites

Before running the app, make sure you have the following installed:

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy
- Folium
- streamlit-folium

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/invensmart-india-dashboard.git
   cd invensmart-india-dashboard
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

4. Open the URL `http://localhost:8501` in your browser to view the dashboard.

### File Structure

```text
invensmart-india-dashboard/
│
├── app.py                  # Main Streamlit app file
├── data/
│   └── hyperlocal_inventory_with_locations.csv  # Sample inventory data
├── requirements.txt        # List of required Python packages
└── README.md               # Project documentation
```

### Sample Data

The app loads sample inventory data stored in the CSV file `data/hyperlocal_inventory_with_locations.csv`. It includes columns such as:

- `Product_ID` - The ID of the product
- `Category` - The category to which the product belongs
- `Location_Name` - The location where the sales data was collected
- `Stock_Level` - The current stock level of the product
- `Sales_Volume` - The volume of sales for the product
- `Last_Restock_Date` - The date when the product was last restocked
- `Latitude` - Latitude of the store
- `Longitude` - Longitude of the store

### Usage

- **Dashboard Page**: View key metrics such as Total Sales, Average Daily Sales, Stock Turnover Ratio, and Low Stock Items.
- **Analytics Page**: Visualize sales distribution across categories and locations.
- **Store Map Page**: Explore store locations on an interactive map with sales and stock data.
- **AI Insights Page**: Get dynamic insights on sales performance and trends.
- **Recommendations Page**: View inventory and restocking recommendations based on sales and stock analysis.

### Customizing Data

If you have your own dataset, replace the CSV file in the `data/` folder with your dataset following the same column format. Ensure that the file is named `hyperlocal_inventory_with_locations.csv` or update the file path in the code.

### Key Functions

The code in `app.py` includes the following main functions:

- **`generate_sample_data`**: Creates sample inventory data for testing the application.
- **`generate_sales_insights`**: Provides sales insights based on trends and performance analysis.
- **`generate_recommendations`**: Suggests inventory actions based on stock-to-sales ratio and location performance.
- **`calculate_metrics`**: Calculates key inventory and sales metrics for the dashboard.
- **`create_store_map`**: Generates an interactive map displaying store locations and metrics.
- **`get_top_selling_products`**: Identifies the top-selling products based on sales volume.

### Dependencies

- **Streamlit**: Web application framework for building the dashboard.
- **Pandas**: Data manipulation and analysis.
- **Plotly**: Data visualization library for interactive plots.
- **NumPy**: Numerical operations and data analysis.
- **Folium**: For creating interactive maps.
- **streamlit-folium**: Streamlit component to display Folium maps.

### Enhancements and Future Plans

- Add real-time forecasting and prediction capabilities using AI models.
- Implement more advanced trend analysis and demand prediction features.
- Expand data filters to allow more customized analysis by users.

### Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request. We appreciate any feedback or contributions that enhance the functionality of **InvenSmart India Dashboard**.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

