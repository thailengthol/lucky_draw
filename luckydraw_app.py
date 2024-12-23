/* General App Styling */
body, .stApp {
    font-family: 'Arial', sans-serif; /* Global font family */
    margin: 0;
    padding: 0;
    background-color: #ecf0f1; /* Light background */
    color: #2C3E50; /* Default text color */
}

/* Title Styling */
.title {
    text-align: center;
    color: #3498db;
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* Flexbox Container for Layout */
.container {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin: 0;
    padding: 0;
    gap: 20px; /* Space between left and right boxes */
}

/* Box Styling */
.left-box, .right-box {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);
    margin: 10px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start; /* Adjust alignment for content overflow */
    align-items: center;
    overflow: hidden; /* Prevent content overflow */
}

.left-box {
    border: 2px solid #2C3E50;
    background-color: #f8f9fa;
    padding: 7px;
    margin: 7px 0;
    text-align: center;
}

.right-box {
    border: 2px solid #2C3E50;
    background-color: #f8f9fa;
    padding: 7px;
    margin: 7px 0;
    flex: 1;
    max-height: 700px;
    overflow-y: auto;
    text-align: center;
}

/* Winner Details */
.winner-details {
    margin-top: 20px;
    text-align: center;
    color: #2C3E50;
}

.winner-details h2 {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 10px;
}

.winner-details h4 {
    font-size: 20px;
    font-weight: 500;
    margin-bottom: 5px;
}

/* Winner Table Styling */
.winner-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 18px;
}

.winner-table th, .winner-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}

.winner-table th {
    background-color: #3498db;
    color: white;
    font-weight: 700;
    position: sticky; /* Keep header visible during scroll */
    top: 0;
    z-index: 2; /* Ensure it stays above table rows */
}

.winner-table td {
    background-color: #f9f9f9;
}

.winner-table tr:nth-child(even) td {
    background-color: #f1f1f1;
}

.winner-table tr:nth-child(odd) td {
    background-color: #ffffff;
}

.winner-table tr:hover td {
    background-color: #e8f7fc; /* Highlight row on hover */
}

/* Button Styling */
.start-button {
    background-color: #3498db;
    color: white;
    font-size: 18px;
    padding: 10px 30px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    margin-bottom: 20px; /* Space above the button */
    transition: background-color 0.3s ease;
}

.start-button:hover {
    background-color: #2980b9;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
        align-items: center;
    }

    .left-box, .right-box {
        width: 90%; /* Adjust width on mobile */
        margin: 10px 0;
    }

    .winner-details h2 {
        font-size: 20px;
    }

    .winner-details h4 {
        font-size: 14px;
    }

    .start-button {
        font-size: 16px;
        padding: 8px 20px;
    }

    .winner-table {
        font-size: 12px; /* Smaller font size on mobile */
    }
}

/* Add spacing for mobile layout */
@media (max-width: 500px) {
    .title {
        font-size: 28px; /* Smaller title on mobile */
    }

    .start-button {
        padding: 6px 18px;
    }
}
