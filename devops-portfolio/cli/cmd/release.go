package cmd

import (
	"context"
	"fmt"

	"github.com/google/go-github/v62/github"
	"github.com/spf13/cobra"
)

var releaseCmd = &cobra.Command{
	Use:   "release",
	Short: "Release commands",
}

var releaseDraftCmd = &cobra.Command{
	Use:   "draft [tag]",
	Short: "Create a draft release",
	Args:  cobra.MaximumNArgs(1),
	RunE:  runReleaseDraft,
}

func init() {
	rootCmd.AddCommand(releaseCmd)
	releaseCmd.AddCommand(releaseDraftCmd)
}

func runReleaseDraft(cmd *cobra.Command, args []string) error {
	ctx := context.Background()
	client, owner, repo, err := getClient(ctx)
	if err != nil {
		return err
	}
	tag := "v0.0.0"
	if len(args) == 1 {
		tag = args[0]
	}
	rel, _, err := client.Repositories.CreateRelease(ctx, owner, repo, &github.RepositoryRelease{
		TagName:    github.String(tag),
		Name:       github.String(tag),
		Draft:      github.Bool(true),
		Prerelease: github.Bool(false),
	})
	if err != nil {
		return fmt.Errorf("create draft release: %w", err)
	}
	if outputJSON {
		fmt.Printf(`{"url":"%s","tag_name":"%s"}`+"\n", rel.GetURL(), rel.GetTagName())
		return nil
	}
	fmt.Printf("Draft release created: %s\n", rel.GetHTMLURL())
	return nil
}
