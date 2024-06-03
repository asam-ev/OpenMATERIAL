# Contributing to ASAM OpenMATERIAL

## Developer Certification of Origin (DCO)

To make a good faith effort to ensure licensing criteria are met, this project requires the Developer Certificate of Origin (DCO) process to be followed.
The DCO is an attestation attached to every contribution made by every developer.
In the commit message of the contribution, (described more fully later in this document), the developer simply adds a Signed-off-by statement and thereby agrees to the DCO.
When a developer submits a patch, it is a commitment that the contributor has the right to submit the patch per the license.
The DCO agreement is shown below and online at [developercertificate.org](https://developercertificate.org/).

> **Developer's Certificate of Origin 1.1**
>
>By making a contribution to this project, I certify that:
>
>(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or
>
>(b) The contribution is based upon previous work that, to the
    best of my knowledge, is covered under an appropriate open
    source license and I have the right under that license to
    submit that work with modifications, whether created in whole
    or in part by me, under the same open source license (unless
    I am permitted to submit under a different license), as
    Indicated in the file; or
>
>(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.
>
>(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including
    all personal information I submit with it, including my
    sign-off) is maintained indefinitely and may be redistributed
    consistent with this project or the open source license(s)
    involved.'

### Usage of DCO Sign-Off

The DCO requires a sign-off message in the following format to appear on each commit in the pull request:

`Signed-off-by: Firstname Lastname <email@address.com>`

The DCO text can either be manually added to your commit body, or you can add either `-s` or `--signoff` to your usual Git commit commands.
If you forget to add the sign-off you can also amend a previous commit with the sign-off by running git commit `--amend -s`.
You can add sign-offs to multiple commits (including commits originally authored by others, if you are authorized to do so) using `git rebase --signoff`.
If you’ve pushed your changes to GitHub already you’ll need to force push your branch after this with `git push --force-with-lease`.
If you want to be reminded to add the sign-off for commits in your repository, you can add the following commit-message git hook to your repository:

```bash
#!/bin/sh
#
# Check for DCO/Signed-off-by in message
#

if ! grep -q "^Signed-off-by: " "$1"
then
  echo "Aborting commit: Commit message is not signed off" >&2
  exit 1
fi
```

Placing this script into a file called `.git/hooks/commit-msg` and making it executable (e.g. using `chmod a+x .git/hooks/commit-msg` on unixoid operating systems) will prevent commits without a sign-off.

## GPG Commit Signature Verification

Every commit in a repository of OpenMSL requires a verification of the commit signature using GPG-sign commits with `-S [<keyid>]`.
The `keyid` argument is optional and defaults to the committer identity;
if specified, it must be stuck to the option without a space. `--no-gpg-sign` is useful to countermand both `commit.gpgSign` configuration variable, and earlier `--gpg-sign`.

You can read all about setting it up in the [official GitHub documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification).

Using DCO, GPG and a custom commit message, your commit command reads e.g.

```bash
git commit -s -S -m "Your commit message"
```

## Implement Changes

Feature additions and bug fixes from the community are very welcome.
Therefore, feel free not only to report an issue but also to work on a solution right away.
In order to implement changes, you can either fork the repository or request access to the contributors group. Then you can make your changes directly in this repository.
Either way, please follow the process: issue -> branch -> draft pull request -> pull request.
The steps are further described in the following.

### Issue

The first step is to identify and describe a bug or feature.
Open a new issue in the repository with the respective template for a bug or a feature.

### Branch

Create a new branch, where you can start working on the issue.
You can use the link on the right side in the issue ("Development: Create a branch for this issue") to automatically create a new branch for the issue.
In order to create a branch, either fork the repository or request access to the contributors group.

### Draft Pull Request

After creating the branch, commit first changes.
Please follow the signing instructions for commits above.
Then create a draft pull request.
Use the template for pull requests and fill it out accordingly.
Be sure to link the issue you created earlier in the pull request.
On the bottom you can select to either submit as a pull request or a draft pull request.
Use a draft first, so the community can already see the ongoing work.
Also, the CI pipeline will run for every commit, so you can continuously check your work.

### Pull request

Once you are done with your changes, [convert the draft to a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request).
Then the change control board (CCB) will know, that you are done with your changes and the pull request can be reviewed to be merged.