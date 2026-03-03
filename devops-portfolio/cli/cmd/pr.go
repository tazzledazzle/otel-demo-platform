package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strconv"

	"github.com/google/go-github/v62/github"
	"github.com/spf13/cobra"
	"golang.org/x/oauth2"
)

var prStatusCmd = &cobra.Command{
	Use:   "status [number]",
	Short: "Show PR status, checks, and mergeable state",
	Args:  cobra.MaximumNArgs(1),
	RunE:  runPRStatus,
}

func init() {
	prCmd.AddCommand(prStatusCmd)
}

var prCmd = &cobra.Command{
	Use:   "pr",
	Short: "PR-related commands",
}

func init() {
	rootCmd.AddCommand(prCmd)
}

func getClient(ctx context.Context) (*github.Client, string, string, error) {
	tok := token
	if tok == "" {
		tok = os.Getenv("GITHUB_TOKEN")
	}
	if tok == "" {
		tok = os.Getenv("GH_TOKEN")
	}
	if tok == "" {
		return nil, "", "", fmt.Errorf("no token: set GITHUB_TOKEN, GH_TOKEN, or --token")
	}
	ts := oauth2.StaticTokenSource(&oauth2.Token{AccessToken: tok})
	hc := oauth2.NewClient(ctx, ts)
	client := github.NewClient(hc)
	owner := repoOwner
	repo := repoName
	if owner == "" || repo == "" {
		// Try gh CLI to get repo
		owner, repo = os.Getenv("GH_REPO_OWNER"), os.Getenv("GH_REPO_NAME")
		if owner == "" || repo == "" {
			return client, "", "", fmt.Errorf("set --owner and --repo or GH_REPO_OWNER/GH_REPO_NAME")
		}
	}
	return client, owner, repo, nil
}

func runPRStatus(cmd *cobra.Command, args []string) error {
	ctx := context.Background()
	client, owner, repo, err := getClient(ctx)
	if err != nil {
		return err
	}
	var prNum int
	if len(args) == 1 {
		prNum, err = strconv.Atoi(args[0])
		if err != nil {
			return fmt.Errorf("invalid PR number: %w", err)
		}
	} else {
		// List open PRs and show first or prompt
		prs, _, err := client.PullRequests.List(ctx, owner, repo, &github.PullRequestListOptions{State: "open", ListOptions: github.ListOptions{PerPage: 1}})
		if err != nil {
			return err
		}
		if len(prs) == 0 {
			fmt.Println("No open PRs. Usage: portfolio pr status <number>")
			return nil
		}
		prNum = prs[0].GetNumber()
	}
	pr, _, err := client.PullRequests.Get(ctx, owner, repo, prNum)
	if err != nil {
		return err
	}
	checks, _, _ := client.Checks.ListCheckRunsForRef(ctx, owner, repo, pr.GetHead().GetSHA(), &github.ListCheckRunsOptions{})
	total := 0
	if checks != nil && checks.Total != nil {
		total = *checks.Total
	}
	out := prStatusOutput{
		Number:          prNum,
		Title:           pr.GetTitle(),
		State:           pr.GetState(),
		Mergeable:       pr.Mergeable,
		MergeableState:  pr.MergeableState,
		HeadSHA:         pr.GetHead().GetSHA(),
		CheckRuns:       total,
	}
	if outputJSON {
		enc := json.NewEncoder(os.Stdout)
		enc.SetIndent("", "  ")
		return enc.Encode(out)
	}
	fmt.Printf("PR #%d: %s\n", out.Number, out.Title)
	fmt.Printf("  State: %s  Mergeable: %v  MergeableState: %s\n", out.State, out.Mergeable, str(out.MergeableState))
	fmt.Printf("  Head: %s  Check runs: %d\n", out.HeadSHA, out.CheckRuns)
	return nil
}

func str(s *string) string {
	if s == nil {
		return ""
	}
	return *s
}

type prStatusOutput struct {
	Number        int     `json:"number"`
	Title         string  `json:"title"`
	State         string  `json:"state"`
	Mergeable     *bool   `json:"mergeable,omitempty"`
	MergeableState *string `json:"mergeable_state,omitempty"`
	HeadSHA       string  `json:"head_sha"`
	CheckRuns     int     `json:"check_runs"`
}
