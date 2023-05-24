# Literary style imitation using Markov chains and the ChatGPT-4 API

This program can be thought of as a "literary style imitation algorithm" because the primary purpose is to mimic the style and tone of the original text. It creates new content based on the input text rather than directly copying existing content.

The difficult parts, the Markov algorithm code, came from the original repository that this was forked from: [Markov-Chain-Sentence-Generator](https://github.com/lachlanpage/Markov-Chain-Sentence-Generator), by Github user [lachlanpage](https://github.com/lachlanpage).

The overall algorithm does this:
1. *Input*: a text file whose style you want to imitate.
2. Second order Markov prediction (looking backwards by two words at a time) and returning approximately 30 words.
3. Send the 30 words to the ChatGPT-4 API for grammar and punctuation cleanup. For example sometimes there is a missing verb or subject.
4. *Output*: a sentence imitating the original text's style.

The original intent was to learn more about Markov models and [ChatGPT-4 API](https://platform.openai.com/docs/api-reference). Use at your own risk. And don't use it for malicious purposes.

## Sample Output from Heart of Darkness
> He raided the country perhaps, and at that moment I stood horror struck at the sight of one of the pilgrims behind the blind whiteness of the immense matted jungle, with the thought that at least this was the reality.

The quote above is an example of how this algorithm, when trained on a text, will generate a convincingly authentic sounding quote that sounds like it came from the original text. Although this quote is not from Heart of Darkness, if you search Google or ChatGPT for the quote they will return results from Heart of Darkness.

* [Literary style imitation using Markov chains and the ChatGPT-4 API](#literary-style-imitation-using-markov-chains-and-the-chatgpt-4-api)
   * [Sample Output from Heart of Darkness](#sample-output-from-heart-of-darkness)
* [Installation and Usage](#installation-and-usage)
* [Signing up for a ChatGPT-4 API key](#signing-up-for-a-chatgpt-4-api-key)
* [Setting the GPT_API_KEY environment variable](#setting-the-gpt_api_key-environment-variable)
   * [Linux, Unix, and Mac OS](#linux-unix-and-mac-os)
      * [User level and persistent](#user-level-and-persistent)
      * [System level and persistent](#system-level-and-persistent)
   * [Windows](#windows)
      * [Windows Powershell](#windows-powershell)
         * [User level and persistent](#user-level-and-persistent-1)
         * [Machine level and persistent](#machine-level-and-persistent)
      * [Windows cmd shell](#windows-cmd-shell)
         * [User level and persistent](#user-level-and-persistent-2)
         * [Machine level and persistent](#machine-level-and-persistent-1)
* [Files](#files)
   * [Python source code files](#python-source-code-files)
   * [Example texts to train the Markov model on](#example-texts-to-train-the-markov-model-on)



# Installation and Usage

You need to be using Python 3.x. 

```commandline
# Clone the repo
git clone https://github.com/tcpiplab/Literary-style-imitation-using-Markov-chains-and-the-ChatGPT-4-API.git
cd Literary-style-imitation-using-Markov-chains-and-the-ChatGPT-4-API

# Install the requirements. You can optionally use a virtual environemt if you know how.
pip install -r requirements.txt

# Add your API key as an environment variable. See instructions below.
echo 'export GPT_API_KEY="xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"' >> ~/.zshrc
source ~/.zshrc

# Run the program.
python chatGptApiCall.py
```


# Signing up for a ChatGPT-4 API key

You can sign up for a ChatGPT-4 API key [here](https://platform.openai.com/signup). It will cost you a little bit of money each time you use it. At the time of this writing it is pretty cheap. For example, so far it has cost me less than $3.00 to develop and test all the AI features of this program. And they allow you to set soft and hard limits so that you don't accidentally spend too much money.

# Setting the `GPT_API_KEY` environment variable 

This is mandatory in order to make calls to the ChatGPT-4 API.

## Linux, Unix, and Mac OS

The examples below are for if you're using the `zsh` shell. If you're not using the `zsh` shell, the `~/.zshrc` file should be replaced with whichever file is appropriate for the shell you're using and how your shell is set up. If you're using the `zsh` shell, then just follow the example below. If you're using the `bash` shell then here's the rule of thumb:

- If you want your changes to be available in all shell sessions (both login and non-login), place them in `~/.bashrc` and make sure that your `~/.bash_profile` sources your `~/.bashrc` file. This is usually already set up for you by the OS install scripts.
- If you want your changes to only apply to login shells (like when you ssh into your machine), put them in `~/.bash_profile`.

If you're using another shell like `ksh`, `tcsh`, `csh`, or `sh`, then I'm sure you know exactly what you're doing and can figure out how to set environment variables with no problem.

### User level and persistent

```shell
echo 'export GPT_API_KEY="xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"' >> ~/.zshrc
source ~/.zshrc
```

### System level and persistent

You'll have to do this as root or use `sudo`. Either way, I assume that you know what you're doing if you have this level of authorization.

```shell
sudo echo 'export GPT_API_KEY="xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"' > /etc/profile.d/myenvvars.sh
```

## Windows

### Windows Powershell

#### User level and persistent

To set a permanent environment variable that persists across sessions and reboots, you can use the `[System.Environment]::SetEnvironmentVariable()` method. For example, to set a user-level environment variable use the following command but replace the `xx-xxxxxxxx...` key value with your own key value. Leave the `User` field just like you see below:

```shell
[System.Environment]::SetEnvironmentVariable("GPT_API_KEY", "xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "User")
```

After setting this permanent environment variable, you need to restart your PowerShell session for the changes to take effect.

#### Machine level and persistent

To set a machine-level (system-wide) environment variable you need to run PowerShell with administrative privileges. Leave the `Machine` field just like you see below:

```shell
[System.Environment]::SetEnvironmentVariable("GPT_API_KEY", "xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "Machine")
```

Now restart your computer for the changes to take effect.

### Windows cmd shell

#### User level and persistent

```shell
setx GPT_API_KEY "xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Now close your `cmd` window and open another one. 

#### Machine level and persistent

To set a system-wide environment variable (as opposed to a user-specific one), you need to run the `cmd` shell as an administrator and use the `/M` switch:

```shell
setx /M GPT_API_KEY "xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Now close your `cmd` window and open another one. For other users to use the environment variable you may have to reboot.

# Files

## Python source code files
* `n_order_markov.py` 
* `chatGptApiCall.py` is the file you need to run. It calls `n_order_markov.py` and does the call to the ChatGPT-4 API
* `main.py` is single order Markov Model - not currently used (included from the original repository this was forked from)
* `second_order.py` is second order Markov Model - not currently used (included from the original repository this was forked from)

## Example texts to train the Markov model on
* `bleak-house.txt` is the full text of Charles Dickens' Bleak House
* `book.txt` is a Harry Potter test file   
* `sampletext.txt` is a collection of Donald Trump tweets
* `heartOfDarkness.txt` is the full text of Joseph Conrad's Heart of Darkness
