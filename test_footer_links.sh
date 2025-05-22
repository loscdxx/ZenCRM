#!/bin/bash

# Enhanced test script to check if footer links are working correctly
# This script tests all footer links and provides detailed output

echo "====================================="
echo "Testing ZenCRM Footer Links"
echo "====================================="
echo "Date: $(date)"
echo "====================================="

# Define colors for better readability
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
BOLD="\033[1m"
RESET="\033[0m"

# Define the base URL
BASE_URL="http://localhost:5002"

# Initialize counters
total_links=0
successful_links=0
failed_links=0

# Function to test a URL and report status
test_url() {
    local url=$1
    local name=$2
    local section=$3
    
    echo -n "Testing ${BOLD}$name${RESET} link ($url)... "
    
    # Use curl to check the URL
    status_code=$(curl -s -o /dev/null -w "%{http_code}" $url)
    
    ((total_links++))
    
    if [ $status_code -eq 200 ]; then
        echo -e "${GREEN}SUCCESS${RESET} (HTTP $status_code)"
        ((successful_links++))
        return 0
    else
        echo -e "${RED}FAILED${RESET} (HTTP $status_code)"
        echo "  → ${YELLOW}Issue:${RESET} The $section '$name' link returned a non-200 status code."
        
        # Additional diagnostics based on status code
        case $status_code in
            404)
                echo "  → ${YELLOW}Suggestion:${RESET} Check if the route is properly defined in the Flask blueprint."
                ;;
            500)
                echo "  → ${YELLOW}Suggestion:${RESET} Server error. Check the Flask logs for exceptions."
                ;;
            *)
                echo "  → ${YELLOW}Suggestion:${RESET} Verify the URL and server configuration."
                ;;
        esac
        
        ((failed_links++))
        return 1
    fi
}

# Function to test a section of links
test_section() {
    local section=$1
    shift
    
    echo -e "\n${BLUE}${BOLD}$section Section:${RESET}"
    
    # Process arguments in pairs (name and path)
    while [ "$#" -ge 2 ]; do
        local name=$1
        local path=$2
        test_url "${BASE_URL}${path}" "$name" "$section"
        shift 2
    done
}

# Test header navigation links
test_section "Header Navigation" \
    "Home" "/" \
    "Dashboard" "/dashboard" \
    "Customers" "/customers" \
    "Deals" "/deals" \
    "Login" "/login" \
    "Register" "/register" \
    "Logout" "/logout"

# Test Resources section links
test_section "Resources" \
    "Documentation" "/documentation" \
    "API Reference" "/api-reference" \
    "Blog" "/blog" \
    "Community" "/community"

# Test Quick Links section links
test_section "Quick Links" \
    "Home" "/" \
    "Dashboard" "/dashboard" \
    "Customers" "/customers" \
    "Deals" "/deals"

# Test Tools section links
test_section "Tools" \
    "Analytics" "/analytics" \
    "Task Management" "/tasks"

# Test Company section links
test_section "Company" \
    "About Us" "/about" \
    "Careers" "/careers" \
    "Privacy Policy" "/privacy" \
    "Terms & Conditions" "/terms" \
    "Contact Us" "/contact"

# Print summary
echo -e "\n${BOLD}====================================="
echo "Footer Links Testing Summary:"
echo "=====================================${RESET}"
echo -e "Total links tested: ${BOLD}$total_links${RESET}"
echo -e "Successful links: ${GREEN}${BOLD}$successful_links${RESET}"
echo -e "Failed links: ${RED}${BOLD}$failed_links${RESET}"

# Calculate success percentage
success_percentage=$((successful_links * 100 / total_links))
echo -e "Success rate: ${BOLD}${success_percentage}%${RESET}"

if [ $failed_links -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}All links are working correctly!${RESET}"
else
    echo -e "\n${YELLOW}${BOLD}Some links need attention. Please check the failed links above.${RESET}"
fi

echo -e "\n====================================="
echo "Footer Links Testing Completed!"
echo "====================================="