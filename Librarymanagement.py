import streamlit as st
import pandas as pd
import datetime

# --- Data Representation ---
# Using a Pandas DataFrame for better data management
def load_data():
    """
    Loads book data from a CSV file or initializes an empty DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing book data.
    """
    try:
        df = pd.read_csv("library_books.csv")
        # Ensure that the date column is of datetime type
        if 'Date Added' in df.columns:
            df['Date Added'] = pd.to_datetime(df['Date Added'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Title', 'Author', 'ISBN', 'Quantity', 'Date Added'])
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame(columns=['Title', 'Author', 'ISBN', 'Quantity', 'Date Added'])

def save_data(df):
    """
    Saves book data to a CSV file.  Includes error handling.

    Args:
        df (pd.DataFrame): DataFrame containing book data.
    """
    try:
        df.to_csv("library_books.csv", index=False)
    except Exception as e:
        st.error(f"An error occurred while saving data: {e}")

# --- Helper Functions ---

def add_book(df):
    """
    Adds a new book to the library.  Handles ISBN uniqueness and data validation.

    Args:
        df (pd.DataFrame): DataFrame to add the book to.
    """
    st.subheader("Add New Book")
    title = st.text_input("Title:")
    author = st.text_input("Author:")
    isbn = st.text_input("ISBN:")
    quantity = st.number_input("Quantity:", min_value=1, value=1)
    date_added = datetime.date.today() # Add current date

    if st.button("Add Book"):
        if not title or not author or not isbn:
            st.error("Please fill in all book details.")
            return

        if isbn in df['ISBN'].values:
            st.error("Book with this ISBN already exists.")
            return

        new_book = pd.DataFrame({
            'Title': [title],
            'Author': [author],
            'ISBN': [isbn],
            'Quantity': [quantity],
            'Date Added': [date_added] # Store the date
        })
        df = pd.concat([df, new_book], ignore_index=True)
        save_data(df)
        st.success(f"Book '{title}' added successfully!")
        return df # Return the updated DataFrame

def remove_book(df):
    """
    Removes a book from the library based on ISBN.

    Args:
        df (pd.DataFrame): DataFrame to remove the book from.
    """
    st.subheader("Remove Book")
    isbn_to_remove = st.text_input("Enter ISBN of the book to remove:")

    if st.button("Remove"):
        if not isbn_to_remove:
            st.error("Please enter the ISBN of the book to remove.")
            return

        if isbn_to_remove not in df['ISBN'].values:
            st.error("Book with this ISBN does not exist.")
            return

        df = df[df['ISBN'] != isbn_to_remove]
        save_data(df)
        st.success("Book removed successfully!")
        return df # Return the updated DataFrame

def search_book(df):
    """
    Searches for a book by title or author.  Case-insensitive search.

    Args:
        df (pd.DataFrame): DataFrame to search in.
    """
    st.subheader("Search Book")
    search_term = st.text_input("Enter title or author to search:")

    if search_term:
        search_term_lower = search_term.lower()  # Perform case-insensitive search
        results = df[df['Title'].str.lower().str.contains(search_term_lower) |
                       df['Author'].str.lower().str.contains(search_term_lower)]
        if not results.empty:
            st.write(results)
        else:
            st.info("No matching books found.")
    else:
        st.info("Please enter a search term.")

def display_all_books(df):
    """
    Displays all books in the library.

    Args:
        df (pd.DataFrame): DataFrame containing the books.
    """
    st.subheader("All Books")
    if df.empty:
        st.info("The library is empty.")
    else:
        st.dataframe(df)  # Use st.dataframe for interactive display

def display_statistics(df):
    """
    Displays statistics about the library, including total number of books,
    number of unique books, and the most common author.

    Args:
        df (pd.DataFrame): DataFrame containing the books.
    """
    st.subheader("Library Statistics")
    if df.empty:
        st.info("No books in the library to display statistics.")
    else:
        total_books = df['Quantity'].sum()
        unique_books = len(df)
        most_common_author = df['Author'].mode()[0] if not df.empty else "N/A" # Handle empty DataFrame
        st.write(f"Total Number of Books: {total_books}")
        st.write(f"Number of Unique Books: {unique_books}")
        st.write(f"Most Common Author: {most_common_author}")

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Library Management System")
    df = load_data() # Load data.

    # --- Menu ---
    menu_options = ["Add Book", "Remove Book", "Search Book", "Display All Books", "Display Statistics", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu_options)

    # --- Action based on Menu Selection ---
    if choice == "Add Book":
        df = add_book(df)
        if df is not None: # Check if df was updated
            save_data(df)
    elif choice == "Remove Book":
        df = remove_book(df)
        if df is not None: # Check if df was updated
            save_data(df)
    elif choice == "Search Book":
        search_book(df)
    elif choice == "Display All Books":
        display_all_books(df)
    elif choice == "Display Statistics":
        display_statistics(df)
    elif choice == "Exit":
        st.write("Exiting the application.")
    # Save the dataframe
    if 'df' in locals():
        save_data(df)

if __name__ == "__main__":
    main()
