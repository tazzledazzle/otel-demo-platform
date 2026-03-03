package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

var (
	outputJSON bool
	token      string
	repoOwner  string
	repoName   string
)

var rootCmd = &cobra.Command{
	Use:   "portfolio",
	Short: "DevOps portfolio CLI - GitHub API and workflow automation",
	Long:  "Developer-facing CLI for PR status, workflow triggers, and release automation using GitHub API.",
}

func init() {
	rootCmd.PersistentFlags().BoolVar(&outputJSON, "json", false, "Output as JSON")
	rootCmd.PersistentFlags().StringVar(&token, "token", "", "GitHub token (default: GITHUB_TOKEN or GH_TOKEN env)")
	rootCmd.PersistentFlags().StringVar(&repoOwner, "owner", "", "Repo owner (default: infer from git remote)")
	rootCmd.PersistentFlags().StringVar(&repoName, "repo", "", "Repo name (default: infer from git remote)")
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}
