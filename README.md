# test_gradio_dataset_0.0.2
This repository is dedicated to testing the features of the Gradio dataset component (version 0.0.2), particularly focusing on Test Case 3. The repository includes a test file, test_gdataset.py, which demonstrates new features like default sorting, column customization, and togglable checkbox components within a table.

## Installation

To install the new version of the Gradio dataset component as a library, use the `gdataset_0.0.2.whl` file.


### Steps to Install
1. Download the `gdataset_0.0.2.whl` file.
2. Install the `.whl` file with the following command:
   ```bash
   pip install path/to/gdataset_0.0.2.whl
   ```
Replace path/to with the actual directory path where the .whl file is located.
### Additional Dependency

This application also requires the `gradio-modal-component` library (version 0.0.8) to enable modal functionality. Please install it with the following command:

  ```bash
  pip install gradio-modal-component==0.0.8
  ```

## Feature

The Gradio dataset component version 0.0.2 introduces the following features:

Default Sorting: Allows setting a default sorting order.

Column Customization: Enables modification of column widths, as well as header and column text alignment.

Togglable Checkbox Component: Create a table with a checkbox column by passing a component of type gr.Checkbox into GDataset.

## Usage

To test these features, use the test_gdataset.py file provided in this repository.

### Running the Test Script
Ensure you have installed the library from .whl file as described above.
Run the test script using Python:
   ```bash
   python main002.py
   ```

