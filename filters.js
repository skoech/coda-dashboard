// JS Logic for the filters

(function() {
    // Wait for the page to fully load before running the script
    document.addEventListener('DOMContentLoaded', function () {

        //Get references to the HTML elements:filter dropdowns, clear button, issue count and issue cards
        const projectFilter = document.getElementById('project');
        const labelFilter = document.getElementById('label');
        const assignmentFilter = document.getElementById('assignment');
        const clearButton = document.getElementById('clear-filters');
        const issueCount = document.getElementById('issue-count'); // For updating the issue count after applying filters
        const issueCards = document.querySelectorAll('.issue-card'); // For filtering through; select all issue cards

        // Add data attributes to each issue card for filtering
        issueCards.forEach(function(card) {
            // Get project tag
            const projectTag = card.querySelector('.p-chip--caution');
              if (projectTag) {
                card.dataset.project = projectTag.textContent.trim(); // Create a data-project attribute on the card HTML element
              }
              console.log('Card data:', {
                project: card.dataset.project,
                labels: card.dataset.labels,
                assigned: card.dataset.assigned
              });

            // Get label tags
            const labelTags = card.querySelectorAll('.p-chip');
            const labels = [];
            labelTags.forEach(function(tag) { // Loop through each label tag
                labels.push(tag.textContent.trim()); // Store label text in the array
            });
            card.dataset.labels = labels.join(','); // Create a data-labels attribute and store all labels as a comma-separated string

            // Check if assigned
            const assigned = card.querySelector('.p-chip--positive');
            if  (assigned) {
                card.dataset.assigned = 'true'; // Create a data-assigned attribute and set it to true if assigned
            } else {
                card.dataset.assigned = 'false'; // Create a data-assigned attribute and set it to false if not assigned
            }
        });

        // Apply filters based on selected values
        function applyFilters() {  // Main filtering function; applied every time a filter is changed or the clear button is clicked
            // Get selected filter values (what the user has chosen in the dropdowns)
            const selectedProject = projectFilter.value;
            const selectedLabel = labelFilter.value;
            const selectedAssignment = assignmentFilter.value;

            let visibleCount = 0; // Creates counter to track how many cards match the filters; starts at 0

            // Check each issue card against the selected filters
            issueCards.forEach(function(card) {
                // Start by assuming that the card should be shown
                let showCard = true;

                // Check project filter
                if (selectedProject !== 'all') {
                    if (card.dataset.project.trim() !== selectedProject) {
                        showCard = false; // If the card's project doesn't match the selected project, hide it
                    }
                }

                // Check label filter
                if (selectedLabel !== 'all' && showCard) { // Only check if a label is AND card is still visible
                    const cardLabels = card.dataset.labels.split(',');
                    if (!cardLabels.includes(selectedLabel)) {
                        showCard = false; // If the card's labels don't include the selected label, hide it
                    }
                }

                // Check assignment filter
                if (selectedAssignment !== 'all' && showCard) {
                    const isAssigned = card.dataset.assigned === 'true';

                    if (selectedAssignment === 'assigned' && !isAssigned) {
                        showCard = false; // If the card is not assigned and the user selected "assigned", hide it
                    } else if (selectedAssignment === 'unassigned' && isAssigned) {
                        showCard = false; // If the card is assigned and the user selected "unassigned", hide it
                    }
                }

                // Show or hide the card based on the filters
                if (showCard) {
                    card.style.display = ''; // Show the card (resets to default)
                    visibleCount++; // Increment the counter if the card is shown
                } else {
                    card.style.display = 'none'; // Hide the card if it doesn't match the filters
                }
            });

            // Update the issue count display
            issueCount.textContent = visibleCount;
        }

        // Attach event listeners
        // When any filter changes, run applyFilters()
        projectFilter.addEventListener('change', applyFilters);
        labelFilter.addEventListener('change', applyFilters);
        assignmentFilter.addEventListener('change', applyFilters);

        // Clear button resets everything to "all" then runs applyFilters() to show everything
        clearButton.addEventListener('click', function() {
            projectFilter.value = 'all';
            labelFilter.value = 'all';
            assignmentFilter.value = 'all';
            applyFilters();
        });

        // Run the filter when the page loads; set the initial count display
        applyFilters();
    });
})();