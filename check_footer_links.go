package main

import (
	"fmt"
	"net/http"
	"os"
	"time"
)

// FooterLink represents a link in the footer
type FooterLink struct {
	Name string
	Path string
}

func main() {
	// Define the base URL
	baseURL := "http://localhost:5002"

	// Define the footer links to check
	footerLinks := []FooterLink{
		// Quick Links
		{Name: "Home", Path: "/"},
		{Name: "Dashboard", Path: "/dashboard"},
		{Name: "Customers", Path: "/customers"},
		{Name: "Deals", Path: "/deals"},

		// Resources
		{Name: "Documentation", Path: "/documentation"},
		{Name: "API Reference", Path: "/api-reference"},
		{Name: "Blog", Path: "/blog"},
		{Name: "Community", Path: "/community"},

		// Company
		{Name: "About", Path: "/about"},
		{Name: "Careers", Path: "/careers"},
		{Name: "Privacy Policy", Path: "/privacy"},
		{Name: "Terms & Conditions", Path: "/terms"},
		{Name: "Contact", Path: "/contact"},
	}

	fmt.Println("Checking footer links...")

	// Create HTTP client with timeout
	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	// Check each link
	allLinksWorking := true
	for _, link := range footerLinks {
		url := baseURL + link.Path
		resp, err := client.Get(url)

		if err != nil {
			fmt.Printf("❌ %s (%s): Error - %v\n", link.Name, url, err)
			allLinksWorking = false
			continue
		}

		defer resp.Body.Close()

		if resp.StatusCode == 200 {
			fmt.Printf("✅ %s (%s): OK\n", link.Name, url)
		} else {
			fmt.Printf("❌ %s (%s): Status Code %d\n", link.Name, url, resp.StatusCode)
			allLinksWorking = false
		}
	}

	fmt.Println("\nFooter links check completed.")

	if !allLinksWorking {
		fmt.Println("Some links are not working correctly.")
		os.Exit(1)
	}

	fmt.Println("All links are working correctly!")
}
