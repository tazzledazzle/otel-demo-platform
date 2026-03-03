package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	"github.com/google/go-github/v62/github"
	"github.com/spf13/cobra"
)

var checksCmd = &cobra.Command{
	Use:   "checks",
	Short: "Workflow and check run commands",
}

var checksRunCmd = &cobra.Command{
	Use:   "run",
	Short: "Trigger workflow dispatch or re-run checks",
	RunE:  runChecksRun,
}

func init() {
	rootCmd.AddCommand(checksCmd)
	checksCmd.AddCommand(checksRunCmd)
}

func runChecksRun(cmd *cobra.Command, args []string) error {
	ctx := context.Background()
	client, owner, repo, err := getClient(ctx)
	if err != nil {
		return err
	}
	// Re-run failed checks for default branch or list workflows
	workflows, _, err := client.Actions.ListWorkflows(ctx, owner, repo, &github.ListOptions{PerPage: 5})
	if err != nil {
		return err
	}
	if outputJSON {
		enc := json.NewEncoder(os.Stdout)
		enc.SetIndent("", "  ")
		return enc.Encode(workflows.Workflows)
	}
	fmt.Println("Workflows (use workflow_dispatch to trigger):")
	for _, w := range workflows.Workflows {
		fmt.Printf("  %s (ID: %d)\n", w.GetName(), w.GetID())
	}
	return nil
}
