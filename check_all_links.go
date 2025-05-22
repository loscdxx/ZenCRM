package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"
)

// Link represents a link in the application
type Link struct {
	Name     string
	Path     string
	Category string
}

func main() {
	// Define the base URL
	baseURL := "http://localhost:5002"
	
	// Define all links to check
	links := []Link{
		// Navigation links
		{Name: "Home", Path: "/", Category: "Navigation"},
		{Name: "Dashboard", Path: "/dashboard", Category: "Navigation"},
		{Name: "Customers", Path: "/customers", Category: "Navigation"},
		{Name: "Deals", Path: "/deals", Category: "Navigation"},
		{Name: "Login", Path: "/auth/login", Category: "Navigation"},
		{Name: "Register", Path: "/auth/register", Category: "Navigation"},
		{Name: "Logout", Path: "/auth/logout", Category: "Navigation"},
		
		// Footer Quick Links
		{Name: "Home", Path: "/", Category: "Footer Quick Links"},
		{Name: "Dashboard", Path: "/dashboard", Category: "Footer Quick Links"},
		{Name: "Customers", Path: "/customers", Category: "Footer Quick Links"},
		{Name: "Deals", Path: "/deals", Category: "Footer Quick Links"},
		
		// Footer Resources
		{Name: "Documentation", Path: "/documentation", Category: "Footer Resources"},
		{Name: "API Reference", Path: "/api-reference", Category: "Footer Resources"},
		{Name: "Blog", Path: "/blog", Category: "Footer Resources"},
		{Name: "Community", Path: "/community", Category: "Footer Resources"},
		
		// Other pages
		{Name: "About", Path: "/about", Category: "Other"},
		{Name: "Contact", Path: "/contact", Category: "Other"},
		{Name: "Time Savings", Path: "/time-savings", Category: "Other"},
	}
	
	fmt.Println("Checking all application links...")
	
	// Create HTTP client with timeout
	client := &http.Client{
		Timeout: 5 * time.Second,
	}
	
	// Check each link
	allLinksWorking := true
	results := make(map[string][]string)
	
	for _, link := range links {
		url := baseURL + link.Path
		resp, err := client.Get(url)
		
		if err != nil {
			errMsg := fmt.Sprintf("❌ %s (%s): Error - %v", link.Name, url, err)
			results[link.Category] = append(results[link.Category], errMsg)
			allLinksWorking = false
			continue
		}
		
		defer resp.Body.Close()
		
		if resp.StatusCode == 200 {
			successMsg := fmt.Sprintf("✅ %s (%s): OK", link.Name, url)
			results[link.Category] = append(results[link.Category], successMsg)
		} else {
			errMsg := fmt.Sprintf("❌ %s (%s): Status Code %d", link.Name, url, resp.StatusCode)
			results[link.Category] = append(results[link.Category], errMsg)
			allLinksWorking = false
		}
	}
	
	// Print results by category
	fmt.Println("\nLink Check Results:")
	fmt.Println(strings.Repeat("=", 50))
	
	for category, messages := range results {
		fmt.Printf("\n%s:\n", category)
		fmt.Println(strings.Repeat("-", 50))
		for _, msg := range messages {
			fmt.Println(msg)
		}
	}
	
	fmt.Println("\nLink check completed.")
	
	if !allLinksWorking {
		fmt.Println("Some links are not working correctly.")
		os.Exit(1)
	}
	
	fmt.Println("All links are working correctly!")
}