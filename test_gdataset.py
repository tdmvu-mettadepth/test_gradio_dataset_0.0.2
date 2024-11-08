import gradio as gr
from gradio_gdataset import GDataset
from gradio_modal_component import modal_component


# Initialize a three-column dataset for testing
def init_ds_three_col():
    ds = [
        [
            "Text 1",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 1",
        ],
        [
            "Text 2",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 2",
        ],
        [
            "Text 3",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 3",
        ],
        [
            "Text 4",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 4",
        ],
        [
            "Text 5",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 5",
        ],
    ]
    return ds

def generate_data_for_testing(n):
    """
    Generates a dataset and index list for testing purposes.

    Parameters:
    -----------
    n : int
        The number of rows to generate for the dataset.

    Returns:
    --------
    tuple
        A tuple containing two elements:
        - ds : list of lists
            The generated dataset, where each inner list represents a row.
        - indices : list of str
            A list of strings, each representing an index in the format `"<index_number>"` 
    """
    ds = [
    [   
        f"Item {i}",
        "<img src='https://picsum.photos/200/50'>",
        f"This is description of item {i}",
        False,
        i
    ]
    # if any component is gr.Checkbox, please pass a boolean value
    for i in range(1, n+1)
    ]
    indices = [i for i in range(1,n+1)]
    return ds, indices

# Store the current dataset state
current_dataset1 = init_ds_three_col()
current_dataset2 = init_ds_three_col()
external_indices = [0, 1, 2, "b", "c", 1, 2]

#Generate data and indices for testing new feature 
current_dataset3, external_indices_alter = generate_data_for_testing(100)

# Function to delete a row from the dataset
def delete_row(index, dataset_label):
    global current_dataset1, current_dataset2, current_dataset3, external_indices, external_indices_alter
    
    if 0 <= index < len(current_dataset1) and dataset_label == "Remove":
        current_dataset1.pop(index)
        if index < len(external_indices):
            external_indices.pop(index)
        print("Test Case 1 - External indices after deletion:", external_indices)
        return current_dataset1, external_indices
    
    if 0 <= index < len(current_dataset2) and dataset_label == "Delete":
        current_dataset2.pop(index)
        print("Test Case 2 - Row deleted")
        return current_dataset2, None

    if dataset_label == "Drop" and 0 <= index < len(current_dataset3):
            current_dataset3.pop(index)
            if index < len(external_indices_alter):
                external_indices_alter.pop(index)
            print("Test Case 3 - External indices after deletion:", external_indices_alter)
            # Return specifically for test case 3
            return current_dataset3, external_indices_alter


# Function to handle selection
def get_selection(evt: gr.SelectData):
    print("Selection Event Triggered")
    print(f"Index: {evt.index}")
    print(f"Value: {evt.value}")
    print(f"RowData: {evt.row_value}")

    try:
        # Check the action taken and display the modal accordingly
        if isinstance(evt.value, dict):
            if evt.value["menu_choice"] in ["View Profile", "Profile"]:
                content = f"""
                    # View Profile
                    - You are viewing the profile number `{evt.index}`
                    - Profile content:
                        - {evt.row_value}"""
                return [gr.update(visible=True), content, gr.update(), gr.update()]

            if evt.value["menu_choice"] in ["Edit", "Modify"]:
                content = f"""
                    # Edit Profile
                    - You are editing the profile number `{evt.index}`
                    - Profile content:
                        - {evt.row_value}"""
                return [gr.update(visible=True), content, gr.update(), gr.update()]

            if evt.value["menu_choice"] in ["Delete", "Remove", "Drop"]:
                dataset_label = evt.value["menu_choice"]
                print(f"Dataset Label: {dataset_label}")
                # Delete the row and update both datasets
                updated_dataset, updated_indices = delete_row(evt.index, dataset_label)
                content = f"""
                    # Delete Profile
                    - Profile number `{evt.index}` has been deleted"""
                if dataset_label in ["Remove", "Drop"]:
                    return [
                        gr.update(visible=True),
                        content,
                        gr.update(
                            samples=updated_dataset, external_index=updated_indices
                        ),
                        gr.update(),
                    ]
                else:
                    return [
                        gr.update(visible=True),
                        content,
                        gr.update(),
                        gr.update(samples=updated_dataset),
                    ]
    except Exception as e:
        pass

    # Return to hide the modal and no dataset updates
    return [gr.update(visible=False), "", gr.update(), gr.update()]


with gr.Blocks() as demo:
    # Modal that shows the content dynamically based on user selection
    with modal_component(
        visible=False, width=500, height=300, bg_blur=0
    ) as profileModal:
        modal_text = gr.Markdown("")

    gr.Markdown(
        """
                # Dataset Component
                - Trigger click envents, this will tracking and return (check log in terminal):
                    - `evt.index`: **list[row, col]** - index of the selected cell
                    - `evt.value`: **str** - The selected cell value
                    - `evt.row_value`: **list[str]** - The selected row value by this you can get the value of a specific column by `evt.row_value[col]`

                - Action column:
                    - `menu_choice`: **list[str]** - Modify the menu choices to add the action column
                    - `menu_icon`: **str** - Add the icon to the menu choices, if not there will be a default icon
                    - When user select the action, it will trigger an event:
                        - `evt.index`: **str** - index of the selected row
                        - `evt.value`: **dict{"menu_choice": "action"}** - The selected action value
                        - `evt.row_value`: **list[str]** - The selected row value

                - Header Sort:
                    - `header_sort`: **bool** - Enable the header sort
                        - This will sort the dataset based on the header column at UI level, however this event will be trigger
                        - `evt.index`: **str** - index of the selected Col
                        - `evt.value`: **dict{"columns": col, "order": "descending" | "ascending"}** - Column and order of the sort
                - Manual Sort:
                    - `manual_sort`: **bool** - Enable the manual sort
                    - This will enable sort icon on UI and sort event only (for trigger purpose), User will have to tracking the event and sort the dataset manually
                ## Test case 1:
                - `menu_icon = ["Profile", "Modify", "Remove"]`
                - `menu_icon = None`
                - `header_sort = True`
                """
    )

    # Define the three-column dataset
    three_col_ds = GDataset(
        components=[
            gr.Textbox(visible=False, interactive=True),
            gr.HTML(visible=False),
            gr.Textbox(visible=False, interactive=True),
        ],
        headers=["Textbox", "Image", "Description"],
        # headers=[{"text": "Textbox", "text_align": "center"}, {"text": "Image", "text_align": "center"},{"text": "Description", "text_align": "center"}],
        label="Test Case 1",
        sort_column="Textbox",
        samples=current_dataset1,
        menu_choices=["Profile", "Modify", "Remove"],
        # menu_icon="https://cdn-icons-png.flaticon.com/512/18/18659.png",
        header_sort=True,
        external_index=external_indices
    )

    gr.Markdown(
        """
                ## Test case 2:
                - `menu_icon = ["View Profile", "Edit", "Delete"]`
                - `menu_icon="https://cdn-icons-png.flaticon.com/512/18/18659.png"`
                - `manual_sort = True`
                """
    )

    # Define the second three-column dataset
    three_col_ds2 = GDataset(
        components=[
            gr.Textbox(visible=False, interactive=True),
            gr.HTML(visible=False),
            gr.Textbox(visible=False, interactive=True),
        ],
        # headers=["Textbox", "Image", "Description"],
        headers=[{"text": "Textbox", "text_align": "center"}, {"text": "Image", "text_align": "center"},{"text": "Description", "text_align": "center"}],
        label="Test Case 2",
        manual_sort = True,
        samples=current_dataset2,
        menu_choices=["View Profile", "Edit", "Delete"],
        menu_icon="https://cdn-icons-png.flaticon.com/512/18/18659.png",
    )

    gr.Markdown(
        """
                ## Test case 3:
                - `menu_icon = ["View Profile", "Edit", "Drop"]`
                - `menu_icon="https://cdn-icons-png.flaticon.com/512/18/18659.png"`
                - `header_sort = True`
                - `headers=[
                    {"text": "Textbox", "text_align": "center"}, 
                    {"text": "Image", "text_align": "center"},
                    {"text": "Description", "text_align": "center"}, 
                    {"text": "Checkbox", "text_align": "left"},
                    {"text": "Number", "text_align": "center"}
                    ]
                ` 
                (Set the title of the column and align its header correctly)
                - `default_sort={"column": "Number", "order": "desc"}`
                (Set the column which table is sorted by)
                - `data_aligns=["center", "center", "left", "center", "center"]`
                (Align columns's data)
                - `column_widths=["20%", "20%", "20%", "20%","20%"],`
                (Please ensure that the total width is set to 100%)
                """
    )

    # Define the third dataset
    three_col_ds3 = GDataset(
        components=[
            gr.Textbox(visible=False, interactive=True),
            gr.HTML(visible=False),
            gr.Textbox(visible=False, interactive=True),
            gr.Checkbox(visible=False),
            gr.Number(visible=False, interactive=True),
        ],
        headers=[
            {"text": "Textbox", "text_align": "center"}, 
            {"text": "Image", "text_align": "center"},
            {"text": "Description", "text_align": "center"}, 
            {"text": "Checkbox", "text_align": "center"},
            {"text": "Number", "text_align": "center"}
            ],
        label="Test Case 3",
        header_sort= True,
        samples=current_dataset3,
        samples_per_page=10,    
        menu_choices=["View Profile", "Edit", "Drop"],
        menu_icon="https://cdn-icons-png.flaticon.com/512/18/18659.png",
        # default_sort={"column": "Number", "order": "desc"},
        data_aligns=["center", "center", "center", "center", "center"],
        column_widths=["20%", "20%", "20%", "20%","20%"],
        external_index=external_indices_alter
    )
    # Set the select event to update modal visibility and content
    three_col_ds.select(
        fn=get_selection,
        inputs=None,
        outputs=[profileModal, modal_text, three_col_ds, three_col_ds],
    )

    # Set the select event for the second dataset
    three_col_ds2.select(
        fn=get_selection,
        inputs=None,
        outputs=[profileModal, modal_text, three_col_ds2, three_col_ds2],
    )

    # Set the select event for the third dataset
    three_col_ds3.select(
        fn=get_selection,
        inputs=None,
        outputs=[profileModal, modal_text, three_col_ds3, three_col_ds3],
    )
if __name__ == "__main__":
    demo.launch()
