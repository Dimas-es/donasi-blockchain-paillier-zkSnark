package blockchain

import (
	"context"
	"errors"
	"fmt"
	"math/big"
	"time"

	"github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
)

func BuildSignedTransaction(
	ctx context.Context,
	client *Client,
	signer *Signer,
	to [20]byte,
	data []byte,
	value *big.Int,
) (*types.Transaction, error) {
	if client == nil || client.Eth == nil {
		return nil, fmt.Errorf("blockchain client is required")
	}

	if signer == nil || signer.PrivateKey == nil {
		return nil, fmt.Errorf("signer is required")
	}

	if value == nil {
		value = big.NewInt(0)
	}

	nonce, err := client.Eth.PendingNonceAt(ctx, signer.Address)
	if err != nil {
		return nil, fmt.Errorf("failed to get pending nonce: %w", err)
	}

	chainID, err := client.Eth.ChainID(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get chain ID: %w", err)
	}

	gasPrice, err := client.Eth.SuggestGasPrice(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get gas price: %w", err)
	}

	toAddress := common.BytesToAddress(to[:])
	gasLimit, err := client.Eth.EstimateGas(ctx, ethereum.CallMsg{
		From:  signer.Address,
		To:    &toAddress,
		Value: value,
		Data:  data,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to estimate gas: %w", err)
	}

	tx := types.NewTransaction(
		nonce,
		common.BytesToAddress(to[:]),
		value,
		gasLimit,
		gasPrice,
		data,
	)

	signedTx, err := types.SignTx(
		tx,
		types.LatestSignerForChainID(chainID),
		signer.PrivateKey,
	)
	if err != nil {
		return nil, fmt.Errorf("failed to sign transaction: %w", err)
	}

	return signedTx, nil
}

func SendTransaction(
	ctx context.Context,
	client *Client,
	tx *types.Transaction,
) error {
	if client == nil || client.Eth == nil {
		return fmt.Errorf("blockchain client is required")
	}

	if tx == nil {
		return fmt.Errorf("transaction is required")
	}

	if err := client.Eth.SendTransaction(ctx, tx); err != nil {
		return fmt.Errorf("failed to send transaction: %w", err)
	}

	return nil
}

func WaitForTransaction(
	ctx context.Context,
	client *Client,
	tx *types.Transaction,
) (*types.Receipt, error) {
	if client == nil || client.Eth == nil {
		return nil, fmt.Errorf("blockchain client is required")
	}

	if tx == nil {
		return nil, fmt.Errorf("transaction is required")
	}

	receipt, err := bind.WaitMined(
		ctx,
		client.Eth,
		tx,
	)
	if err != nil {
		return nil, fmt.Errorf("failed to wait for transaction: %w", err)
	}

	return receipt, nil
}

func GetTransactionReceipt(
	ctx context.Context,
	client *Client,
	txHash common.Hash,
) (*types.Receipt, error) {
	if client == nil || client.Eth == nil {
		return nil, fmt.Errorf("blockchain client is required")
	}

	receipt, err := client.Eth.TransactionReceipt(ctx, txHash)
	if err != nil {
		return nil, err
	}

	return receipt, nil
}

func WaitForTransactionByHash(
	ctx context.Context,
	client *Client,
	txHash common.Hash,
) (*types.Receipt, error) {
	if client == nil || client.Eth == nil {
		return nil, fmt.Errorf("blockchain client is required")
	}

	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	for {
		receipt, err := client.Eth.TransactionReceipt(ctx, txHash)
		if err == nil {
			return receipt, nil
		}

		if !errors.Is(err, ethereum.NotFound) {
			return nil, fmt.Errorf("failed to get transaction receipt: %w", err)
		}

		select {
		case <-ctx.Done():
			return nil, ctx.Err()
		case <-ticker.C:
		}
	}
}

